# CHANGELOG

本文件记录本项目（CommunityManagerAgent / Gatsby）每次文件增删改查的变更，写清「为什么改」和「改了什么」。版本号以项目根 `VERSION` 文件为唯一权威（当前 0.1.0）。

## [未发布]

### 变更

- **群公告纳入版本管理**：`.gitignore` 由整目录忽略 `docs/` 改为白名单放行——只放行 `docs/community/announcement.md`，其余 docs 内容（运营日志、群聊整理、复盘等含群成员个人信息的运行时数据）仍忽略。**为什么**：用户裁定群公告后续要做版本迭代（群规与定位随运营演进），需要进 git 跟踪；同步去掉 announcement.md 头部「.gitignore 忽略、本地保存」的过时说明，改为「随运营迭代版本化」。

## [0.1.0] - 2026-08-25

### 新增（项目立项：微信社群运营 Agent CommunityManagerAgent）

- **为什么建**：用户的微信社群（以 AI 为纽带的跨界互帮互助交流群）需要专职运营——群公告已定调「后续运营理念和方法主要由微信社群运营智能体负责，本人为辅助、引导和执行角色」，新建专职 agent 承接；用户裁定其不分组、直属用户（团队五小组之外）。拟人名 Gatsby 查注册表无重复，名字取自《了不起的盖茨比》的传奇派对主人（办活动、聚人气、造氛围的极致文化符号）。
- **改了什么**：按团队脚手架新建全套——根 `CLAUDE.md`（角色定义 + 社群定位 + 工作原则，CLAUDE.md 放项目根、跟随 Kit 项目同日进行中的 `.claude/CLAUDE.md` → 根 `CLAUDE.md` 迁移形态）、`README.md` / `README_cn.md` 双语（含 Gatsby 名字出处与社群定位）、`assets/logo.svg`（金色渐变 #F59E0B → #B45309 + 🥂，各项目配色查重无撞色）、`VERSION`（0.1.0）、`CHANGELOG.md`、`TODO.md` / `TODO-archive.md`（冷启动运营包与复盘机制两条待办）、`LICENSE.md`（MIT）、`.gitignore`、`.claude/settings.json` / `settings.local.json` / `settings.local.example.json` 三件套；`git init` 本地初始化（未建远程）。关联同步：全局 `~/.claude/CLAUDE.md` 注册表加 Gatsby 行 + 流水线段补直属说明（CapabilityManagerAgent `claude/CLAUDE.md` 镜像随全局对齐）；xhqing 主页 roster 双语加行 + `scripts/update_traffic.py` 团队清单加 CommunityManagerAgent + 预建徽章 JSON（细节记 xhqing 自己的 CHANGELOG）。
