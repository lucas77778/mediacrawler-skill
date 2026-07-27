# mediacrawler-skill

给 Claude Code、Codex 等 AI agent 用的 [Agent Skills](https://agentskills.io)：

| Skill | 能力 |
|---|---|
| [`mediacrawler`](skills/mediacrawler/SKILL.md) | 用 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 爬取小红书、抖音、快手、B 站、微博、贴吧、知乎的内容、评论和创作者数据。首次使用自动浅克隆并安装，无需手动部署 |
| [`seedance`](skills/seedance/SKILL.md) | 调用火山方舟 Seedance API 生成视频：请求体组装、prompt 约束、提交轮询下载、抽帧质检、多段拼接 |

## 安装

```bash
npx skills add lucas77778/mediacrawler-skill        # 项目级，交互选择 skill
npx skills add lucas77778/mediacrawler-skill -g     # 用户级
```

或手动复制 `skills/<name>/` 到 agent 的 skill 目录（`.claude/skills/`、`.agents/skills/` 等）。

## 使用

对 agent 说「爬取抖音关键词 xx 的视频和评论」或「用 Seedance 生成一段视频」即可自动触发。

- `mediacrawler` 前置：`git`、`uv`、Chrome/Edge；首次登录各平台需扫码。国内网络可设 `MEDIACRAWLER_REPO`（Gitee 镜像源）、`UV_DEFAULT_INDEX`（PyPI 镜像）
- `seedance` 前置：`python3`、`ffmpeg`、火山方舟 `ARK_API_KEY`（按量计费）

## 许可

`mediacrawler` skill 与上游 MediaCrawler 一致：NON-COMMERCIAL LEARNING LICENSE 1.1，仅限学习研究，不得商用或对平台造成运营干扰。
