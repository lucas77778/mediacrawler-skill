# jsonl 输出字段

文件命名：`data/<平台>/jsonl/<模式>_contents_<日期>.jsonl`（帖子）、`<模式>_comments_<日期>.jsonl`（评论）。同日多次运行**追加写入**，需按 ID 去重（`jq -s 'unique_by(.aweme_id)'`）。

字段随平台略有差异。首次分析前先探明实际字段：

```bash
head -1 <file>.jsonl | jq 'keys'
```

## 抖音 contents（已验证）

| 字段 | 说明 |
|---|---|
| `aweme_id` | 视频 ID（其他平台为 `note_id`/`video_id` 等） |
| `title` / `desc` | 标题 / 文案 |
| `liked_count` `comment_count` `share_count` `collected_count` | 互动数据，**字符串类型**，比较时需 `|tonumber` |
| `create_time` | 发布时间戳（秒） |
| `nickname` / `creator_hash` | 作者昵称 / 作者标识 |
| `aweme_url` | 视频页 URL |
| `video_download_url` `cover_url` `music_download_url` | 媒体直链 |
| `source_keyword` | search 模式的来源关键词（detail 模式为空） |
| `last_modify_ts` | 爬取时间戳（毫秒） |

## 抖音 comments（已验证）

| 字段 | 说明 |
|---|---|
| `comment_id` / `aweme_id` | 评论 ID / 所属视频 ID |
| `content` | 评论内容 |
| `like_count` / `sub_comment_count` | 点赞数 / 楼中楼数量 |
| `parent_comment_id` | 二级评论的父评论 ID（一级为空） |
| `nickname` `create_time` `pictures` | 作者 / 时间戳 / 评论图片 |

其他平台字段结构类似（帖子 ID、互动计数、作者、URL、`source_keyword`、`last_modify_ts` 均有对应字段），字段名以实际文件为准；模型定义在 `model/m_<平台>.py`。
