---
name: mediacrawler
description: 用 MediaCrawler 爬取小红书、抖音、快手、B 站、微博、贴吧、知乎的笔记/视频、评论和创作者主页数据，支持关键词搜索、指定帖子详情、创作者主页三种模式。当用户要爬取/采集/搜索这些平台的内容、评论、爆款数据，或提到 MediaCrawler、xhs、douyin 爬虫时使用。
license: 本 skill 与 MediaCrawler 同为 NON-COMMERCIAL LEARNING LICENSE 1.1，仅限学习研究
compatibility: 需要 git、uv、Chrome/Edge（CDP 模式）。首次运行自动下载 MediaCrawler（约 30 MB）；首次登录需人工扫码
metadata:
  upstream: https://github.com/NanmiCoder/MediaCrawler
---

# MediaCrawler 爬虫

爬取中文社媒平台数据。核心模型：**跑一条命令 → 结果落盘为 jsonl → 用 jq 分析文件**。爬虫是一次性批处理进程，跑完即退出。

统一入口是本 skill 的 `scripts/crawl.sh`（下文写作 `crawl.sh`，实际执行用相对本文件的路径），参数原样透传给 MediaCrawler 的 `main.py`。首次运行自动完成安装：浅克隆仓库到 `~/.mediacrawler`（若当前目录已是 MediaCrawler 仓库则直接使用）+ `uv sync` + 代理环境下补装 socksio。

环境变量（按需设置，均可选）：

| 变量 | 用途 |
|---|---|
| `MEDIACRAWLER_HOME` | 自定义安装目录（默认 `~/.mediacrawler`） |
| `MEDIACRAWLER_REPO` | 替换克隆源，如 Gitee 镜像（国内无代理时 GitHub 不稳定） |
| `UV_DEFAULT_INDEX` | PyPI 镜像，如 `https://pypi.tuna.tsinghua.edu.cn/simple` |

## 三种爬取模式

平台代码：`xhs`（小红书）| `dy`（抖音）| `ks`（快手）| `bili`（B 站）| `wb`（微博）| `tieba`（贴吧）| `zhihu`（知乎）。各平台 ID/URL 格式差异见 [references/platforms.md](references/platforms.md)。

**关键词搜索**：

```bash
crawl.sh --platform dy --type search \
  --keywords "关键词1,关键词2" \
  --crawler_max_notes_count 20 --get_comment true \
  --save_data_option jsonl --headless true
```

**指定帖子详情**（评论采集的主力模式）：

```bash
crawl.sh --platform dy --type detail \
  --specified_id "视频ID或URL,可逗号分隔多个" \
  --get_comment true --max_comments_count_singlenotes 50 \
  --save_data_option jsonl --headless true
```

**创作者主页**：

```bash
crawl.sh --platform dy --type creator \
  --creator_id "创作者ID或主页URL" \
  --save_data_option jsonl --headless true
```

常用参数：`--crawler_max_notes_count`（帖子数上限，默认 15）、`--max_comments_count_singlenotes`（单帖一级评论上限，默认 10）、`--get_sub_comment true`（二级评论，默认关）、`--save_data_option`（jsonl/csv/sqlite/excel 等，推荐 jsonl；需去重查询时用 sqlite）。

## 登录与登录态

- **首次登录**：去掉 `--headless true`（即有头模式）运行，浏览器会弹出二维码。提示用户用对应平台 App 扫码，登录完成后爬取自动继续。
- **登录态持久化**：保存在安装目录 `browser_data/` 下的平台用户目录。之后即可用 `--headless true` 无人值守运行。
- **无人值守备选**：`--lt cookie --cookies "<cookie串>"`。
- **注意**：想控制无头与否，一律显式传 `--headless` 参数——它会覆盖配置文件里的 `HEADLESS` 和 `CDP_HEADLESS`，只改配置文件可能被 CLI 默认值覆盖。

## 输出位置与分析

`crawl.sh` 启动时会在 stderr 打印运行目录。结果写入 `<运行目录>/data/<平台全名>/`（目录用全名：`douyin`、`kuaishou`、`bilibili`、`xhs`、`weibo`、`tieba`、`zhihu`）：

```
data/douyin/
├── jsonl/
│   ├── search_contents_2026-07-20.jsonl   # <模式>_contents_<日期>.jsonl 帖子/视频
│   └── search_comments_2026-07-20.jsonl   # <模式>_comments_<日期>.jsonl 评论
└── videos/                                # 媒体文件（ENABLE_GET_MEIDAS 开启时）
```

**分析原则：不要把整个 jsonl 读进上下文**，用 jq 抽取所需字段：

```bash
# 按点赞数排序取 Top10 标题
jq -s 'sort_by(-(.liked_count|tonumber))[:10] | .[] | {title, liked_count, aweme_url}' \
  data/douyin/jsonl/search_contents_*.jsonl

# 某视频的高赞评论
jq -c 'select(.aweme_id=="xxx") | {content, like_count}' data/douyin/jsonl/*_comments_*.jsonl
```

字段说明见 [references/output-schema.md](references/output-schema.md)。同日多次运行会追加到同一文件，注意用 ID 去重。

## 排障

| 症状 | 处理 |
|---|---|
| CDP 连接超时 / `connect ECONNREFUSED 127.0.0.1:9222` | 本机有全局代理；`crawl.sh` 已设 NO_PROXY，若绕过脚本直跑需自行加 `NO_PROXY="localhost,127.0.0.1"` |
| 报缺 `socksio` | 在安装目录 `uv pip install socksio`（`uv sync` 后会丢失） |
| 找不到浏览器 | 在安装目录 `config/base_config.py` 设置 `CUSTOM_BROWSER_PATH` |
| 反复要求扫码、滑块验证 | 用有头模式运行，人工过验证后重试 |
| 登录态失效 | 删除安装目录 `browser_data/` 对应平台目录后重新扫码 |
| 依赖异常 | 删除安装目录 `.venv/` 后重跑（bootstrap 会重新 `uv sync`） |

## 合规约束（必须遵守）

MediaCrawler 是 NON-COMMERCIAL LEARNING LICENSE，仅限学习研究。默认并发 1（`MAX_CONCURRENCY_NUM`），不要调高；单次爬取量保持克制（建议 `--crawler_max_notes_count` ≤ 50）；不得用于商业用途或对平台造成运营干扰。用户要求大规模爬取时，提醒其许可证与风控风险。
