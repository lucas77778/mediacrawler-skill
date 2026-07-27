"""提交 Seedance 视频生成任务，轮询至完成并下载。

用法:
    export ARK_API_KEY=xxx   # 或写入 ~/.ark_api_key（chmod 600）
    python3 submit_seedance.py req_segA.json req_segB.json

请求体 JSON 中可用占位符 {{FILE:相对路径}}（相对于该 JSON 文件），
会被替换为对应图片/音频的 data URI base64，用于 reference_image 等。
每个请求的成片保存为 <json同目录>/<json文件名去掉req_前缀>.mp4。
"""
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.request

BASE = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"


def api_key() -> str:
    if os.environ.get("ARK_API_KEY"):
        return os.environ["ARK_API_KEY"]
    keyfile = os.path.expanduser("~/.ark_api_key")
    if os.path.exists(keyfile):
        with open(keyfile) as fp:
            return fp.read().strip()
    sys.exit("缺少 ARK_API_KEY 环境变量（或 ~/.ark_api_key 文件）")


def api(method: str, url: str, payload=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {api_key()}")
    req.add_header("Content-Type", "application/json")
    data = json.dumps(payload).encode() if payload is not None else None
    with urllib.request.urlopen(req, data=data) as resp:
        return json.loads(resp.read())


def load_request(json_path: str) -> dict:
    here = os.path.dirname(os.path.abspath(json_path))
    with open(json_path, encoding="utf-8") as fp:
        raw = fp.read()

    def embed(m):
        p = os.path.join(here, m.group(1))
        mime = mimetypes.guess_type(p)[0] or "application/octet-stream"
        with open(p, "rb") as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

    return json.loads(re.sub(r"\{\{FILE:([^}]+)\}\}", embed, raw))


def run(json_path: str) -> str:
    name = re.sub(r"^req_", "", os.path.splitext(os.path.basename(json_path))[0])
    task = api("POST", BASE, load_request(json_path))
    print(f"[{name}] 任务已提交: {task['id']}")
    while True:
        time.sleep(15)
        info = api("GET", f"{BASE}/{task['id']}")
        print(f"[{name}] {info['status']}")
        if info["status"] == "succeeded":
            out = os.path.join(os.path.dirname(os.path.abspath(json_path)), f"{name}.mp4")
            urllib.request.urlretrieve(info["content"]["video_url"], out)
            print(f"[{name}] 已下载: {out}")
            return out
        if info["status"] in ("failed", "expired"):
            raise RuntimeError(f"[{name}] 任务{info['status']}: {info.get('error', info)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    files = [run(p) for p in sys.argv[1:]]
    print("\n".join(files))
