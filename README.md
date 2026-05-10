# fastmcp-learning-demo

## Project Overview

`fastmcp-learning-demo` 是一个独立的 FastMCP / MCP 学习项目。

它通过一组小 Demo，学习 MCP Server、Tool、Client、HTTP Transport、Resource、Prompt 和简单 Workflow。

这是学习项目，不是生产系统。

项目不接入真实 LLM，不接入真实 QuoteAgent，不使用数据库，也不做部署配置。

## Learning Goals

本项目用于学习：

- FastMCP Server
- MCP Tool
- MCP Client
- HTTP Transport
- CLI `inspect` / `list`
- MCP Resource
- MCP Prompt
- Tool + Resource + Prompt workflow
- QuoteAgent-style simulated workflow

## What This Project Demonstrates

当前已完成的 Demo：

- `hello` Tool：最小 Tool 示例。
- `calculate_quote_price` Tool：本地假价格规则的报价计算。
- Error handling demo：演示错误参数调用和结构化错误返回。
- `project://summary` Resource：只读项目摘要。
- `analyze_quote_request` Prompt：报价需求分析提示模板。
- Resource → Prompt → Tool workflow demo：组合 MCP 能力的模拟 Agent 流程。
- QuoteAgent-style simulation demo：完整与不完整报价请求的模拟处理流程。

## Project Structure

```text
fastmcp-learning-demo/
  src/
    server.py
    client.py
    client_error_demo.py
    client_resource_demo.py
    client_prompt_demo.py
    client_agent_workflow_demo.py
    client_quote_agent_simulation_demo.py

  docs/
    context/      项目事实和边界
    guides/       环境与验证指南
    rules/        Tool 设计和错误处理规则
    learning/     按步骤整理的学习笔记
    logs/         简洁开发记录
```

## Environment

本项目使用：

- Python 3.12
- uv
- FastMCP
- MCP

约定：

- 使用 `pyproject.toml` 管理依赖。
- 使用 `uv.lock` 锁定依赖版本。
- 不使用全局 `pip install`。
- 不创建 `requirements.txt`。
- 不使用 Docker。

详细环境说明见：

```text
docs/guides/ENVIRONMENT.md
```

## How to Run

### 1. 检查环境

```bash
uv run fastmcp version
```

### 2. 启动 Server

```bash
uv run python src/server.py
```

Server 地址：

```text
http://127.0.0.1:8000/mcp
```

### 3. 运行 Demo Client

另开一个终端运行：

```bash
uv run python src/client.py
uv run python src/client_error_demo.py
uv run python src/client_resource_demo.py
uv run python src/client_prompt_demo.py
uv run python src/client_agent_workflow_demo.py
uv run python src/client_quote_agent_simulation_demo.py
```

### 4. CLI 检查

```bash
uv run fastmcp inspect src/server.py
uv run fastmcp list src/server.py
```

更完整的验证说明见：

```text
docs/guides/TESTING.md
```

## MCP Concepts in This Project

| 概念 | 可以理解为 | 本项目例子 |
| --- | --- | --- |
| Tool | 可调用的动作 | `calculate_quote_price` |
| Resource | 可读取的上下文资料 | `project://summary` |
| Prompt | 可复用的 AI 指令模板 | `analyze_quote_request` |
| Client / Workflow | 串联能力的调用方和流程控制器 | `client_quote_agent_simulation_demo.py` |

简单记法：

- Tool 负责做事。
- Resource 负责提供资料。
- Prompt 负责提供分析指令。
- Client / Workflow 负责把它们按顺序用起来。

## Relationship to QuoteAgent

本项目借用了 QuoteAgent 风格的报价业务场景。

但它只是本地学习 Demo：

- 不接入真实 QuoteAgent。
- 不调用 ASP.NET Core API。
- 不读取真实邮箱。
- 不连接数据库。
- 不接入真实 LLM。

QuoteAgent 风格 Demo 的目的，是帮助理解 MCP 能力如何服务业务 Agent 工作流。

## Documentation Map

- `docs/context/PROJECT_CONTEXT.md`：项目事实、目标和边界。
- `docs/guides/ENVIRONMENT.md`：uv、Python 和依赖管理说明。
- `docs/guides/TESTING.md`：环境、CLI 和各 Demo 的验证命令。
- `docs/rules/MCP_TOOL_DESIGN.md`：Tool 设计规则。
- `docs/rules/ERROR_HANDLING.md`：错误处理规则。
- `docs/learning/`：按步骤整理的学习笔记。
- `docs/logs/DEV_LOG.md`：简洁开发记录。

## Project Status

当前项目已完成 Step 0 到 Step 10。

- Step 0：项目初始化。
- Step 1-8：FastMCP / MCP 核心 Demo。
- Step 9：CLI inspect / list / 测试与文档整理。
- Step 10：项目总结与 README 优化。

## Notes / Boundaries

- This is not a production system.
- This project does not use a real LLM.
- This project does not connect to a real QuoteAgent system.
- This project does not use a database.
- This project does not provide a Web API.
- This project focuses on learning MCP concepts through small demos.
