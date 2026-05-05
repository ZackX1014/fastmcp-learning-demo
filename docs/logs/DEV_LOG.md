# Dev Log

## 2026-05-04

### Step 0：初始化 uv 环境、文档驱动项目结构和学习记录文档

- 变更：
  - 初始化独立项目 `fastmcp-learning-demo`。
  - 固定 Python 版本为 3.12。
  - 添加 FastMCP 依赖。
  - 创建基础目录、文档和占位代码文件。

- 文件：
  - `.python-version`
  - `.gitignore`
  - `pyproject.toml`
  - `uv.lock`
  - `AGENTS.md`
  - `README.md`
  - `docs/context/PROJECT_CONTEXT.md`
  - `docs/guides/ENVIRONMENT.md`
  - `docs/guides/TESTING.md`
  - `docs/rules/MCP_TOOL_DESIGN.md`
  - `docs/rules/ERROR_HANDLING.md`
  - `docs/logs/DEV_LOG.md`
  - `src/server.py`
  - `src/client.py`

- 验证：
  - `uv run fastmcp version`
  - `uv run python src/server.py`
  - `uv run python src/client.py`

- 结果：
  - 已通过。
  - FastMCP version: 3.2.4。
  - MCP version: 1.27.0。
  - Python version: 3.12.13。
  - Server 和 Client 占位入口均可执行。

### Step 1：创建最小可运行的 FastMCP Server，并添加 hello tool

- 变更：
  - 创建 `FastMCP("fastmcp-learning-demo")` Server 实例。
  - 使用 `@mcp.tool` 注册 `hello(name: str) -> dict`。
  - Server 默认使用 HTTP Transport，绑定 `127.0.0.1:8000`。
  - `hello` 正常输入返回成功结构，空白输入返回 `name is required`。

- 文件：
  - `src/server.py`
  - `docs/learning/CORE_CONCEPTS.md`
  - `docs/logs/DEV_LOG.md`

- 验证：
  - `uv run python src/server.py`
  - `uv run fastmcp inspect src/server.py`
  - `uv run fastmcp list src/server.py`
  - `uv run python -c 'from src.server import hello; print(hello("Alice")); print(hello("   "))'`
  - `uv run fastmcp call src/server.py hello name=Alice --json`
  - `uv run fastmcp call src/server.py hello name='   ' --json`

- 结果：
  - 已通过。
  - Server 成功启动在 `http://127.0.0.1:8000/mcp`。
  - `inspect` 显示 Tools 数量为 1。
  - `list` 显示 `hello(name: str) -> dict`。
  - 正常输入返回 `Hello, Alice!`。
  - 空白输入返回 `name is required`。

## 2026-05-05

### Step 1.1：优化核心学习笔记的可复习性

- 变更：
  - 将核心概念文档从偏正式说明调整为复习笔记风格。
  - 补充 MCP Client 和 Tools / Resources / Prompts 的区别。

- 文件：
  - `docs/learning/CORE_CONCEPTS.md`
  - `docs/logs/DEV_LOG.md`

- 验证：
  - `sed -n '1,260p' docs/learning/CORE_CONCEPTS.md`
  - `rg "^## |^### " docs/learning/CORE_CONCEPTS.md`
  - `git diff -- src/server.py src/client.py`

- 结果：
  - 已通过。
  - 核心概念文档包含要求的概念和复习结构。
  - 未修改 `src/server.py` 和 `src/client.py`。

### Step 1.2：拆分学习文档为按步骤编号的笔记文件

- 变更：
  - 将学习笔记入口改为 `docs/learning/README.md`。
  - 新增 Step 1 学习笔记文件。
  - 删除 `docs/learning/CORE_CONCEPTS.md`。
  - 更新 `AGENTS.md` 的学习笔记维护规则。

- 文件：
  - `AGENTS.md`
  - `docs/learning/README.md`
  - `docs/learning/001-fastmcp-server-and-hello-tool.md`
  - `docs/learning/CORE_CONCEPTS.md`
  - `docs/logs/DEV_LOG.md`

- 验证：
  - `find docs/learning -maxdepth 1 -type f -print`
  - `sed -n '1,120p' docs/learning/README.md`
  - `sed -n '1,160p' docs/learning/001-fastmcp-server-and-hello-tool.md`
  - `test ! -f docs/learning/CORE_CONCEPTS.md`
  - `rg "docs/learning/README.md|CORE_CONCEPTS" AGENTS.md docs`

- 结果：
  - 已通过。
  - `docs/learning/README.md` 和 `001-fastmcp-server-and-hello-tool.md` 已创建。
  - `docs/learning/CORE_CONCEPTS.md` 已删除。
  - `AGENTS.md` 已改为读取 `docs/learning/README.md`。
  - 未修改 `src/server.py` 和 `src/client.py`。

### Step 2：创建 MCP Client，通过 HTTP 调用 hello tool

- 变更：
  - 使用 FastMCP `Client` 创建最小 MCP Client。
  - Client 连接 `http://127.0.0.1:8000/mcp`。
  - Client 调用 `hello` Tool，传入 `{"name": "FastMCP"}`。
  - Client 打印 `result.structured_content`。
  - 新增 Step 2 学习笔记并更新学习笔记索引。

- 文件：
  - `src/client.py`
  - `docs/learning/README.md`
  - `docs/learning/002-mcp-client-calls-hello-tool.md`
  - `docs/logs/DEV_LOG.md`

- 验证：
  - `uv run fastmcp inspect src/server.py`
  - `uv run fastmcp list src/server.py`
  - `uv run python src/server.py`
  - `uv run python src/client.py`
  - `uv run python -m py_compile src/client.py src/server.py`

- 结果：
  - 已通过。
  - `inspect` 显示 Tools 数量为 1。
  - `list` 显示 `hello(name: str) -> dict`。
  - Server 成功运行在 `http://127.0.0.1:8000/mcp`。
  - Client 成功输出 `{"success": true, "data": {"message": "Hello, FastMCP!"}}`。
  - 沙箱内直接访问 `127.0.0.1:8000` 受限；使用本机 loopback 权限运行 Client 后验证通过。
