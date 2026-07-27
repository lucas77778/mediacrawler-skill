---
name: seedance
description: 调用火山方舟 Seedance API 生成视频（文生视频、带参考图的图生视频、多段生成拼接），含 prompt 写法约束、报错处理和抽帧质检。当用户要"生成视频/文生视频/跑 Seedance/doubao-seedance"时使用。
compatibility: 需要 python3、ffmpeg（质检与拼接）、火山方舟 ARK_API_KEY；按量计费
---

# Seedance 视频生成

流程：写分镜 prompt → 组装请求体 JSON → `scripts/submit_seedance.py` 提交并下载 → 抽帧质检 →（多段时）拼接。

## 前置

- **ARK_API_KEY**：环境变量或 `~/.ark_api_key` 文件（`chmod 600`，建议后者，不进对话记录）。若 key 曾出现在对话记录中，提醒用户到控制台作废重建。
- **开通门槛**：Seedance 2.0 系列需账户余额 >200 元或购买资源包。
- **模型选择**：`doubao-seedance-2-0-mini-260615` 上限 720p，便宜；要 1080p 换 `doubao-seedance-2-0-260128`（prompt 无需改动）。2.0 系列不支持 seed。

## 请求体

每段视频写成一个 `req_<名字>.json`，`{{FILE:相对路径}}` 占位符会被脚本替换为 base64 data URI：

```json
{
  "model": "doubao-seedance-2-0-mini-260615",
  "content": [
    {"type": "text", "text": "<分镜prompt>"},
    {"type": "image_url", "role": "reference_image", "image_url": {"url": "{{FILE:ref.png}}"}}
  ],
  "resolution": "720p", "ratio": "9:16", "duration": 15,
  "generate_audio": true, "watermark": false
}
```

**参考图要求**：宽高比 [0.4, 2.5]，边长 [300, 6000]px；带噪点背景或水印的图先清理再喂，否则污染画面；**参考图/参考视频禁含真人人脸**（Seedance 2.0 硬限制）。

## Prompt 写法约束

- 结构：整体风格一句 + 按【镜头N，起-止秒】逐镜写，中文 <500 字
- 口播台词放双引号内（驱动 `generate_audio` 输出同步人声）
- 需要参考图元素入画的镜头写「参考图1的…」
- **不要在画面里要求小字文本**（手机屏幕、竖排花字必乱码）；大号横排花字 4~8 字可以

## 提交生成

```bash
python3 scripts/submit_seedance.py req_segA.json req_segB.json
```

放后台跑（720p/15s 每段约 2~3 分钟），成片自动下载到 JSON 同目录。注意事项：

- `SetLimitExceeded`：账户「安全体验模式」限额 → 用户去[开通管理](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement)对**该模型**调高/关闭，改完直接重跑（可挂 60s 间隔自动重试兜底生效延迟）
- 任务 ID 仅存 7 天；视频 URL 有时效，脚本已做完成即下载

## 抽帧质检

对成片做 3×3 contact sheet，用 Read 逐张检查：

```bash
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
ffmpeg -y -v error -i "$f" -vf "fps=9/$dur,scale=320:-1,tile=3x3" -frames:v 1 out.jpg
```

检查项：人物跨镜头一致性、参考图元素还原度、花字错字、物体畸变。中文小字乱码属模型通病 → 记录时间点，后期压字幕覆盖，不值得重跑；分镜结构错误才重跑对应段。

## 多段拼接

单任务时长有限，长视频拆成多段生成；相邻段的分镜用天然场景切换衔接，避免依赖尾帧串联。拼接：

```bash
ffmpeg -y -i segA.mp4 -i segB.mp4 -filter_complex \
"[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac -b:a 128k final.mp4
```
