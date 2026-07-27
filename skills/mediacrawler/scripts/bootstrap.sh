#!/usr/bin/env bash
# 定位或自动安装 MediaCrawler。stdout 只输出安装目录路径，日志走 stderr。
set -euo pipefail

log() { echo "[mediacrawler-skill] $*" >&2; }

is_repo() { [[ -f "$1/main.py" && -d "$1/media_platform" ]]; }

REPO_URL="${MEDIACRAWLER_REPO:-https://github.com/NanmiCoder/MediaCrawler.git}"
DIR="${MEDIACRAWLER_HOME:-$HOME/.mediacrawler}"

if is_repo "$PWD"; then
  DIR="$PWD"
elif ! is_repo "$DIR"; then
  command -v git >/dev/null || { log "需要 git，请先安装"; exit 1; }
  log "首次使用：浅克隆 ${REPO_URL} 到 ${DIR}（约 30 MB；国内网络可设 MEDIACRAWLER_REPO 指向 Gitee 镜像）"
  git clone --depth 1 "$REPO_URL" "$DIR" 1>&2
fi

command -v uv >/dev/null || { log "需要 uv：curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

cd "$DIR"
if [[ ! -d .venv ]]; then
  log "安装依赖（uv sync，国内网络可设 UV_DEFAULT_INDEX 指向 PyPI 镜像）"
  uv sync 1>&2
fi

# shell 有 socks 代理时 httpx 需要 socksio；它不在 pyproject 里，uv sync 后会丢失
if [[ -n "${all_proxy:-}${ALL_PROXY:-}" ]]; then
  uv pip show socksio >/dev/null 2>&1 || uv pip install socksio 1>&2
fi

echo "$DIR"
