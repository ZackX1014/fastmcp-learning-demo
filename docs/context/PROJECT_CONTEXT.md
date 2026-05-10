# Project Context

## 项目目标

`fastmcp-learning-demo` 是一个独立 FastMCP / MCP 学习项目，用于通过 Demo 快速理解 MCP Server、Tool、Client、Resource、Prompt 和 Workflow 的基本闭环。

## 当前阶段

当前已完成 Step 0 到 Step 10。

- Step 0：项目初始化。
- Step 1-8：FastMCP / MCP 核心 Demo。
- Step 9：CLI inspect / list / 测试与文档整理。
- Step 10：项目总结与 README 优化。

## 学习范围

- 创建 FastMCP Server。
- 暴露 MCP Tool。
- 使用 Client 调用 Tool。
- 使用 HTTP 运行。
- 使用 CLI inspect / list 检查。
- 使用 Resource 提供上下文资料。
- 使用 Prompt 提供可复用指令模板。
- 组合 Tool、Resource、Prompt 模拟 Agent 工作流。
- 完成 QuoteAgent 风格的本地模拟 Demo。

## 暂不包含范围

- 不接入真实 QuoteAgent 项目。
- 不调用 ASP.NET Core API。
- 不引入数据库。
- 不接入真实邮箱。
- 不实现认证授权。
- 不做部署配置。
- 不创建 Docker 配置。

## 最终 Demo 目标

输入报价请求文本，使用本地简单规则模拟信息完整性判断，根据本地假价格规则计算报价，并返回结构化结果。

## 与 QuoteAgent 的关系

本项目只做 QuoteAgent 风格模拟，用于学习 MCP Tool 的业务建模方式，不直接集成或依赖真实 QuoteAgent 项目。
