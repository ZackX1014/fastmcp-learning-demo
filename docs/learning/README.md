# Learning Notes

## 本目录用途

本目录用于保存 FastMCP / MCP 学习过程中的核心笔记。

这里不写开发流水账。开发过程记录放在 `docs/logs/DEV_LOG.md`。

这里也不写长篇规范。每份笔记都应该方便复习。

## 学习笔记命名规则

- 每个步骤一个文件。
- 文件名格式：`三位编号-核心内容.md`。
- 编号对应学习步骤。
- 文件名使用英文 kebab-case。

示例：

- `001-fastmcp-server-and-hello-tool.md`
- `002-mcp-client-calls-tool.md`
- `003-quote-price-calculator-tool.md`

## 当前学习笔记目录

1. `001-fastmcp-server-and-hello-tool.md`：最小 FastMCP Server、`hello` Tool、HTTP 运行、CLI inspect / list。
2. `002-mcp-client-calls-hello-tool.md`：MCP Client 通过 HTTP 调用 `hello` Tool，理解 Client / Server 调用闭环。
3. `003-quote-price-calculator-tool.md`：业务型报价计算 Tool，输入校验、结构化返回和 Client 调用示例。
4. `004-tool-validation-and-error-handling.md`：验证 Tool 输入校验、错误调用 Demo 和业务错误边界。
5. `005-mcp-resource-project-summary.md`：MCP Resource、只读项目摘要和 Client 读取 Resource。
6. `006-mcp-prompt-quote-analysis.md`：MCP Prompt、报价分析提示模板和 Client 获取 Prompt。

## 后续维护原则

- 一个步骤原则上对应一份学习笔记。
- 新增核心知识点时，优先更新对应步骤文件。
- 不要把所有知识堆到一个大文件。
- 笔记要通俗、短句、能复习。
- 每个概念尽量结合本项目中的代码或命令。
- 如果一个知识点跨多个步骤，可以在后续步骤文件中补充新的理解。
