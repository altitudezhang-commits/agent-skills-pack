# Aider + OpenRouter 免费路由（本地定版）

用途：需要一个 git 原生结对编程 harness 做小修复/小改动时，用 Aider 经 OpenRouter `:free` 模型 $0 干活（2026-11-12 冒烟实证：20 秒完成一处边界 bug 修复＋自动提交＋复跑测试通过）。难活仍归 Codex；本技能只走轻量代码活，不碰股票打分与涉钱判断。

## 定版组合（照抄，不要改）

- 安装：独立 venv `~/workspace/tools/aider_smoke/venv`（aider-chat 0.86.2，2026-11-12 装）。
- Key：永不落盘、永不打印。运行时现场铸 surrogate 注入环境变量：
  `export OPENROUTER_API_KEY=$(python3 ~/workspace/skills/openrouter/bin/or_key_minter.py)`
- 必须剥 no_proxy（httpx 的 IPv6 no_proxy 坑会让请求挂起）：命令前加 `env -u no_proxy -u NO_PROXY`。
- 非交互跑法：
  `env -u no_proxy -u NO_PROXY ~/workspace/tools/aider_smoke/venv/bin/aider --model openrouter/cohere/north-mini-code:free --message "<一次性指令>" --yes-always`
  在目标 git 仓库目录内运行；Aider 会自动提交，事后以 `git log`/`git diff HEAD~1` 验 diff 为凭。
- 已验真可用的 `:free` 模型（2026-11-12 实拉目录，全目录仅 13 个 `:free`，阵容会轮换——调用前先拉 `GET https://openrouter.ai/api/v1/models` 确认 ID 还在册）：
  - `cohere/north-mini-code:free`（256K，冒烟用的就是它）
  - `recursive/flint-v1.0:free`（262K，编码向）
  - `openrouter/free`（200K，自动路由兜底）
- 额度纪律：OpenRouter 免费池 20 RPM、**50 次/天**（用户定版不充 $10，不按 1,000 次/天算账）；遇 429 是共享池限流，先换 `:free` 模型、再错峰，别连锤。

## 边界

- 免费模型只做轻量代码活与初稿；产出必须以 diff＋测试复跑验收，不看口头汇报。
- OpenCode（opencode-ai 1.19.5）**已于 2026-11-13 定版关账、不再复试**：VM 上 `opencode run` 三试挂死；复验路 A 无新版可升（npm latest 仍 1.19.5），路 B Simular Box 运行时正常但 Zen 免费额度被网关判耗尽、且 key 无合法注入方式。详见 TOOL_REGISTRY OpenCode 行。
- 冒烟证据：~/workspace/research_notes/cli_agents_smoke_20261112.md
