# 各平台 ID / URL 格式

`--specified_id`（detail 模式）与 `--creator_id`（creator 模式）接受的格式因平台而异。权威示例在 `config/<平台>_config.py` 里，以下为要点：

| 平台 | CLI 代码 | 数据目录 | detail 接受 | creator 接受 |
|---|---|---|---|---|
| 小红书 | `xhs` | `data/xhs/` | **必须**完整 URL，含 `xsec_token` 和 `xsec_source` 参数 | 同样需带 `xsec_token` 的主页 URL |
| 抖音 | `dy` | `data/douyin/` | 视频 ID（aweme_id）或视频 URL | sec_user_id（`MS4wLj` 开头）或主页 URL |
| B 站 | `bili` | `data/bilibili/` | BV 号或视频 URL | 数字 UID 或 `space.bilibili.com` URL |
| 快手 | `ks` | `data/kuaishou/` | 视频 ID 或 URL | 用户 ID 或 URL |
| 微博 | `wb` | `data/weibo/` | 微博 ID 或 URL | 用户 ID 或 URL |
| 贴吧 | `tieba` | `data/tieba/` | 帖子 ID 或 `/p/<id>` URL（自动归一化） | 主页 URL 或 portrait id（自动补全） |
| 知乎 | `zhihu` | `data/zhihu/` | 回答/文章 URL | 用户主页 URL |

## 平台注意事项

- **小红书**：不带 `xsec_token` 的裸 note_id 会 404。token 从浏览器地址栏或上一次 search 结果的 `note_url` 字段获取，有时效性，失效后需重新搜索获取。海外版（rednote.com）在 `config/base_config.py` 打开 `XHS_INTERNATIONAL = True`。
- **抖音**：风控最敏感的平台之一，首次登录扫码后可能出现手机号验证，需有头模式人工处理。
- **多个 ID**：逗号分隔，如 `--specified_id "id1,id2,id3"`。
- 各平台还有专属配置项（如排序方式、发布时间过滤），见对应 `config/<平台>_config.py`。
