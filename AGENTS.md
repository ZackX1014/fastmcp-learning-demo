# AGENTS.md

## 任务前必读

Codex 每次执行本项目任务前，必须先阅读以下文档：

1. `docs/context/PROJECT_CONTEXT.md`
2. `docs/guides/ENVIRONMENT.md`
3. `docs/rules/MCP_TOOL_DESIGN.md`
4. `docs/rules/ERROR_HANDLING.md`
5. `docs/guides/TESTING.md`
6. `docs/learning/README.md`
7. `docs/logs/DEV_LOG.md`

## 开发原则

- 每次只推进一个明确步骤。
- 优先保证能运行。
- 不要过度设计。
- 不要接入真实 QuoteAgent 项目。
- 不要引入数据库。
- 不要引入认证。
- 不要提前做部署。
- 不要创建 Docker 配置。
- 不要创建 `requirements.txt`。
- 所有命令优先使用 `uv run`。
- 修改后必须说明如何验证。
- 完成后必须更新 `DEV_LOG.md`。
- `DEV_LOG.md` 只记录简洁开发事实。
- `DEV_LOG.md` 不记录下一步建议。
- `DEV_LOG.md` 不记录长篇原理解释。
- 如果产生新的核心知识点，必须新增或更新对应编号的学习笔记文件。
- 不要恢复或继续使用 `CORE_CONCEPTS.md` 作为学习笔记入口。
- 学习笔记文件采用“编号 + 核心内容”的文件名。
- 一个步骤原则上对应一个学习笔记文件。
- 每个开发步骤完成后必须进行原理解释。
