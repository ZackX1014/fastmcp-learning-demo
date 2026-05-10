# 001 FastMCP Server And Hello Tool

## 这一步学什么

这一步先建立 MCP 的最小起点：

1. 创建一个 FastMCP Server。
2. 注册一个最简单的 `hello` Tool。
3. 用 HTTP 模式运行 Server。
4. 用 `inspect` / `list` 检查 Server 暴露的能力。

这一步还不关心业务报价。

重点是理解：普通 Python 函数如何变成 MCP Client 可以发现和调用的能力。

## 最小闭环

```text
Python function
  -> @mcp.tool
  -> FastMCP Server
  -> CLI inspect/list 可发现
  -> 后续 Client 可调用
```

## FastMCP Server

一句话理解：

FastMCP Server 可以理解为“给 MCP Client 暴露能力的服务容器”。

在普通 Python 项目里，函数通常只在代码内部被调用。

FastMCP Server 做的事，是把这些函数登记起来，并按 MCP 的方式暴露出去。

这样 Client 才能知道：

- Server 叫什么。
- 有哪些 Tool。
- 每个 Tool 需要什么参数。
- 返回结果大概是什么结构。

本项目中的例子：

```python
mcp = FastMCP("fastmcp-learning-demo")
```

这行代码创建了当前学习项目的 Server。

后续的 Tool、Resource、Prompt 都会挂在这个 Server 上。

## MCP Tool

一句话理解：

MCP Tool 可以理解为“Client 可以调用的一个明确动作”。

Tool 通常应该像一个动词动作。

比如：

- 打招呼。
- 计算报价。
- 读取价格。
- 解析报价请求。

Step 1 的 Tool 很小：

```python
hello(name: str) -> dict
```

它只做一件事：接收 `name`，返回问候语。

这虽然简单，但已经具备 Tool 的基本形态：

- 有名称。
- 有输入参数。
- 有返回值。
- 被注册到 Server。

## `@mcp.tool`

一句话理解：

`@mcp.tool` 可以理解为“把普通 Python 函数登记成 MCP Tool 的标记”。

本项目中的写法：

```python
@mcp.tool
def hello(name: str) -> dict:
    ...
```

没有 `@mcp.tool` 时，`hello` 只是一个普通 Python 函数。

加上 `@mcp.tool` 后，FastMCP 会把它登记到 Server 里。

登记之后，Client 才能发现它、查看它、调用它。

注意：

`@mcp.tool` 不负责启动 Server。

它只负责注册 Tool。

真正启动 Server 的是：

```python
mcp.run(...)
```

## Python 装饰器和 `@mcp.tool`

`@mcp.tool` 本质上是 Python 装饰器。

装饰器可以理解为：

在不改变函数主体写法的情况下，给函数额外增加一层能力。

这里增加的能力就是：

“把这个函数交给 FastMCP 管理，并暴露为 MCP Tool。”

所以这不是注释。

注释只给人看。

装饰器会真的影响程序运行。

## 参数类型和 docstring

Tool 参数最好写清楚类型。

比如：

```python
def hello(name: str) -> dict:
```

`name: str` 告诉 FastMCP 和 Client：

这个 Tool 需要一个字符串参数。

docstring 也很重要。

它告诉调用方：

这个 Tool 是做什么的。

在 MCP 场景里，类型注解和 docstring 不只是给人看。

它们也会帮助 Client 理解 Server 暴露的能力。

## 结构化返回

本项目约定 Tool 返回结构化 `dict`。

成功时：

```python
{"success": True, "data": {"message": "Hello, FastMCP!"}}
```

失败时：

```python
{"success": False, "error": "name is required"}
```

为什么不用单纯字符串？

因为业务系统更需要稳定字段。

Client 可以根据 `success` 判断是否成功。

也可以稳定读取 `data` 或 `error`。

这比直接返回一句自然语言更适合后续业务流程。

## HTTP Transport

Transport 可以理解为“Client 和 Server 通信的方式”。

Step 1 使用 HTTP：

```python
mcp.run(transport="http", host="127.0.0.1", port=8000)
```

启动后地址是：

```text
http://127.0.0.1:8000/mcp
```

这里不是普通网页地址。

它是 FastMCP Server 的 MCP 通信入口。

后续 Client 会连接这个地址。

## inspect 和 list

`inspect` 用来查看 Server 概况。

```bash
uv run fastmcp inspect src/server.py
```

它适合确认：

- Server 能不能被加载。
- 有多少 Tools。
- 有多少 Resources。
- 有多少 Prompts。

`list` 用来快速查看 Tool 列表。

```bash
uv run fastmcp list src/server.py
```

在当前 FastMCP 版本里，`list` 主要显示 Tool。

Step 1 里应该能看到 `hello`。

## Tools / Resources / Prompts 简单区别

先记一个粗略版本：

- Tool：执行动作。
- Resource：读取资料。
- Prompt：提供 AI 指令模板。

Step 1 只实现 Tool。

Resource 和 Prompt 会在后续步骤学习。

## 在本项目中的完整例子

`src/server.py` 中：

```python
@mcp.tool
def hello(name: str) -> dict:
    """Return a greeting message for the provided name."""
    if not name.strip():
        return {"success": False, "error": "name is required"}

    return {"success": True, "data": {"message": f"Hello, {name}!"}}
```

## 如何验证

检查 Server：

```bash
uv run fastmcp inspect src/server.py
```

检查 Tool：

```bash
uv run fastmcp list src/server.py
```

启动 Server：

```bash
uv run python src/server.py
```

预期：

- `inspect` 能看到 Server 信息。
- `list` 能看到 `hello`。
- Server 启动在 `http://127.0.0.1:8000/mcp`。

## 容易混淆的点

- FastMCP Server 不是普通 REST API。
- Tool 不是随便一个 Python 函数，必须注册到 Server。
- `@mcp.tool` 是注册 Tool，不是启动 Server。
- HTTP Transport 用 HTTP 通信，但传的是 MCP 协议消息。
- Step 1 只验证 Server 和 Tool 能被发现，还没有完成 Client 调用闭环。
