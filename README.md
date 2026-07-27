# mediacrawler-skill

[MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 的 [Agent Skill](https://agentskills.io) 封装：让 Claude Code、Codex 等 AI agent 直接爬取小红书、抖音、快手、B 站、微博、贴吧、知乎的内容、评论和创作者数据。

Skill 本体只有几个 markdown 和 shell 脚本。首次使用时自动浅克隆 MediaCrawler 到 `~/.mediacrawler` 并安装依赖，无需手动部署。

## 安装

```bash
npx skills add <owner>/mediacrawler-skill        # 项目级
npx skills add <owner>/mediacrawler-skill -g     # 用户级
```

或手动复制 `skills/mediacrawler/` 到 agent 的 skill 目录（`.claude/skills/`、`.agents/skills/` 等）。

## 使用

对 agent 说「爬取抖音关键词 xx 的视频和评论」即可自动触发。前置要求：`git`、`uv`、Chrome/Edge；首次登录各平台需扫码。

国内网络可设 `MEDIACRAWLER_REPO`（Gitee 镜像源）、`UV_DEFAULT_INDEX`（PyPI 镜像），详见 [SKILL.md](skills/mediacrawler/SKILL.md)。

## 许可

与上游 MediaCrawler 一致：NON-COMMERCIAL LEARNING LICENSE 1.1，仅限学习研究，不得商用或对平台造成运营干扰。
