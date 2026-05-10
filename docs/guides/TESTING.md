# Testing

## 用途

本文件用于记录当前学习项目的手动验证命令。

它不是生产测试规范。

它的目标是让学习者能按顺序复现：

- 环境是否可用。
- Server 是否能启动。
- CLI 是否能看到 MCP 能力。
- 各个 Client Demo 是否能跑通。

## 环境检查

```bash
uv run fastmcp version
```

用途：

- 确认 FastMCP 已安装。
- 确认当前命令运行在 uv 管理的 Python 环境中。
- 查看 FastMCP、MCP、Python 和 Platform 信息。

## 启动 Server

```bash
uv run python src/server.py
```

预期：

- FastMCP Server 正常启动。
- HTTP 地址为 `http://127.0.0.1:8000/mcp`。

运行 Client Demo 前，需要先保持 Server 运行。

## CLI 检查

### inspect

```bash
uv run fastmcp inspect src/server.py
```

用途：

- 检查 Server 是否能被 FastMCP 正确加载。
- 查看当前 Server 暴露了多少 Tool、Resource、Prompt。

当前预期：

- Tools 数量为 2。
- Resources 数量为 1。
- Prompts 数量为 1。

### list

```bash
uv run fastmcp list src/server.py
```

用途：

- 快速查看当前 Server 暴露的 Tool 列表。

当前 FastMCP 3.2.4 中，`list` 主要显示 Tool。

当前预期能看到：

- `hello`
- `calculate_quote_price`

Resource 和 Prompt 建议通过 `inspect` 检查：

- Resource：`project://summary`
- Prompt：`analyze_quote_request`

## Client Demo 验证命令

运行下面命令前，先启动 Server：

```bash
uv run python src/server.py
```

### 正常 Tool 调用 Demo

```bash
uv run python src/client.py
```

验证：

- `hello` Tool 可以被调用。
- `calculate_quote_price` Tool 可以用正常参数返回结构化报价结果。

### 错误调用 Demo

```bash
uv run python src/client_error_demo.py
```

验证：

- `quantity = 0` 会返回清晰错误。
- `product_type` 为空会返回清晰错误。
- `urgency = rush` 会返回清晰错误。
- 程序不会在第一个错误场景后直接退出。

### Resource 读取 Demo

```bash
uv run python src/client_resource_demo.py
```

验证：

- Client 可以读取 `project://summary`。
- 输出中能看到项目摘要信息。

### Prompt 获取 Demo

```bash
uv run python src/client_prompt_demo.py
```

验证：

- Client 可以获取 `analyze_quote_request` Prompt。
- 输出中能看到报价需求分析提示模板。

### Tool + Resource + Prompt 工作流 Demo

```bash
uv run python src/client_agent_workflow_demo.py
```

验证：

- Client 可以按 Resource → Prompt → Tool 的顺序串联 MCP 能力。
- 输出中能看到最终模拟 Agent 工作流结果。

### QuoteAgent 风格模拟流程 Demo

```bash
uv run python src/client_quote_agent_simulation_demo.py
```

验证：

- 完整报价请求会调用 `calculate_quote_price`。
- 不完整报价请求不会调用 Tool。
- 不完整报价请求会输出 `missing_fields`。

## 当前 MCP 能力清单

### Tools

- `hello`
- `calculate_quote_price`

### Resource

- `project://summary`

### Prompt

- `analyze_quote_request`

## 每次完成后需要说明

- 修改了什么。
- 执行了哪些验证命令。
- 验证结果是什么。
- 是否建议提交 Git。
