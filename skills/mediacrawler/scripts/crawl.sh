#!/usr/bin/env bash
# MediaCrawler 统一入口，参数原样透传给 main.py。
# 用法示例: crawl.sh --platform dy --type search --keywords "xx" --headless true
set -euo pipefail

DIR="$("$(cd "$(dirname "$0")" && pwd)/bootstrap.sh")"
cd "$DIR"
echo "[mediacrawler-skill] 运行目录: ${DIR}（数据输出在 ${DIR}/data/）" >&2

# NO_PROXY 防止本机代理拦截 CDP 的本地调试端口
exec env NO_PROXY="localhost,127.0.0.1" uv run main.py "$@"
