# Dev Log

## 2026-05-04

### Step 0：初始化 uv 环境、文档驱动项目结构和学习记录文档

#### 完成内容

- 使用 uv 初始化独立项目 `fastmcp-learning-demo`。
- 固定 Python 版本为 3.12。
- 使用 `pyproject.toml` 管理依赖。
- 使用 `uv.lock` 锁定依赖版本。
- 添加 FastMCP 依赖。
- 创建文档驱动开发目录结构。
- 创建核心学习记录文档 `docs/learning/CORE_CONCEPTS.md`。
- 创建开发日志 `docs/logs/DEV_LOG.md`。
- 创建 `src/server.py` 和 `src/client.py` 最小占位文件。

#### 验证状态

- 已完成 uv 项目初始化。
- 已完成 FastMCP 依赖安装。
- 已运行 `uv run fastmcp version`，验证结果：
  - FastMCP version: 3.2.4
  - MCP version: 1.27.0
  - Python version: 3.12.13
- 已运行 `uv run python src/server.py`，占位入口可执行。
- 已运行 `uv run python src/client.py`，占位入口可执行。

#### 下一步建议

Step 1：实现最小 FastMCP Server，但暂不加入复杂业务逻辑。

### Step 1：创建最小可运行的 FastMCP Server，并添加 hello tool

#### 本步骤目标

- 创建最小可运行的 FastMCP Server。
- 添加一个 `hello` Tool。
- 使用 HTTP 模式运行 Server。
- 使用 `fastmcp inspect` 和 `fastmcp list` 检查 Server 暴露的能力。

#### 修改文件

- `src/server.py`
- `docs/learning/CORE_CONCEPTS.md`
- `docs/logs/DEV_LOG.md`

#### 实现内容

- 创建 `FastMCP("fastmcp-learning-demo")` Server 实例。
- 使用 `@mcp.tool` 注册 `hello(name: str) -> dict`。
- `hello` 正常输入时返回 `{"success": True, "data": {"message": "Hello, <name>!"}}`。
- `hello` 收到空字符串或空白字符串时返回 `{"success": False, "error": "name is required"}`。
- Server 默认使用 HTTP Transport，绑定 `127.0.0.1:8000`。

#### 如何验证

```bash
uv run python src/server.py
uv run fastmcp inspect src/server.py
uv run fastmcp list src/server.py
```

也可以临时直接调用函数验证返回结构：

```bash
uv run python -c 'from src.server import hello; print(hello("Alice")); print(hello("   "))'
```

也可以使用 FastMCP CLI 直接调用 Tool：

```bash
uv run fastmcp call src/server.py hello name=Alice --json
uv run fastmcp call src/server.py hello name='   ' --json
```

#### 验证状态

- 已运行 `uv run python src/server.py`，Server 成功启动在 `http://127.0.0.1:8000/mcp`。
- 已运行 `uv run fastmcp inspect src/server.py`，显示 Tools 数量为 1。
- 已运行 `uv run fastmcp list src/server.py`，显示 `hello(name: str) -> dict`。
- 已直接调用 `hello("Alice")`，返回成功结构。
- 已直接调用 `hello("   ")`，返回 `name is required` 错误结构。
- 已运行 `uv run fastmcp call src/server.py hello name=Alice --json`，返回成功结构。
- 已运行 `uv run fastmcp call src/server.py hello name='   ' --json`，返回 `name is required` 错误结构。

#### 下一步建议

Step 2：创建最小 Client，通过 MCP Client 调用 `hello` Tool，理解 Client 与 Server 的调用闭环。

### Step 1.1：优化核心学习笔记的可复习性

#### 本步骤目标

- 优化 `docs/learning/CORE_CONCEPTS.md` 的阅读体验。
- 将偏正式的概念说明改成更适合初学者复习的学习笔记。
- 补充 MCP Client 和 Tools / Resources / Prompts 的区别。

#### 修改文件

- `docs/learning/CORE_CONCEPTS.md`
- `docs/logs/DEV_LOG.md`

#### 为什么优化 CORE_CONCEPTS.md

`CORE_CONCEPTS.md` 是学习沉淀文档，不是企业规范文档。

初学阶段更重要的是能反复看懂、能和当前项目对应起来，而不是追求一次性覆盖所有细节。

#### 优化后的文档风格

- 使用“一句话理解”先建立直觉。
- 使用“通俗解释”降低抽象度。
- 使用“在本项目中的例子”把概念落到代码和命令上。
- 使用“为什么重要”说明学习价值。
- 使用“如何验证”保持可操作。
- 使用“容易混淆的点”帮助区分相近概念。

#### 如何验证

```bash
sed -n '1,260p' docs/learning/CORE_CONCEPTS.md
```

重点检查：

- 是否包含 FastMCP Server、MCP Tool、`@mcp.tool`、Tool 参数类型、Tool 结构化返回、HTTP Transport、MCP Client、`fastmcp inspect`、`fastmcp list`。
- 是否包含 Tools / Resources / Prompts 的区别。
- 是否没有修改 `src/server.py` 和 `src/client.py`。

#### 验证状态

- 已完成 `CORE_CONCEPTS.md` 结构优化。
- 已补充 MCP Client 概念。
- 已补充 Tools / Resources / Prompts 的区别。
- 未修改 `src/server.py`。
- 未修改 `src/client.py`。

#### 下一步建议

Step 2：创建最小 Client，通过 MCP Client 调用 `hello` Tool，理解 Client 与 Server 的调用闭环。
