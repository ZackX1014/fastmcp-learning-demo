# Core Concepts

## 这份笔记怎么用

这不是正式规范文档。

它是学习 FastMCP / MCP 时用来反复复习的核心概念笔记。

这里不记录每一步做了什么。那些内容放在 `docs/logs/DEV_LOG.md`。

这里重点记录：

- 一个概念可以理解为什么。
- 它在本项目里长什么样。
- 为什么它重要。
- 怎么确认自己真的懂了。
- 它容易和什么混淆。

## 复习顺序

建议按这个顺序复习：

1. FastMCP Server
2. MCP Tool
3. `@mcp.tool`
4. Tool 参数类型
5. Tool 结构化返回
6. HTTP Transport
7. MCP Client
8. `fastmcp inspect`
9. `fastmcp list`
10. Tools / Resources / Prompts 的区别

## FastMCP Server

### 一句话理解

FastMCP Server 可以理解为“给 AI 暴露能力的服务容器”。

### 通俗解释

普通 Python 项目里，函数通常只给代码自己调用。

FastMCP Server 做的事，是把这些能力收集起来，并按 MCP 协议暴露出去。

这样 MCP Client 就能知道：

- 这个 Server 叫什么。
- 它有哪些 Tool。
- 每个 Tool 怎么调用。
- 调用后会返回什么。

### 在本项目中的例子

`src/server.py` 里有这一行：

```python
mcp = FastMCP("fastmcp-learning-demo")
```

它创建了当前学习项目的 FastMCP Server。

### 为什么重要

因为 MCP 的第一步不是写业务逻辑，而是先有一个能承载能力的 Server。

没有 Server，Tool 就没有地方注册，Client 也不知道去哪里发现能力。

### 如何验证

运行：

```bash
uv run fastmcp inspect src/server.py
```

如果能看到 Server 名称和组件数量，说明 Server 能被 FastMCP 正确加载。

### 容易混淆的点

FastMCP Server 不等于普通 Web API。

普通 Web API 通常面向 HTTP 路由，比如 `/users`、`/orders`。

FastMCP Server 面向 MCP Client，重点是暴露 Tool、Resource、Prompt 这些 AI 可用能力。

## MCP Tool

### 一句话理解

MCP Tool 可以理解为“AI Client 可以调用的一个具体动作”。

### 通俗解释

Tool 通常对应一个动词动作。

比如：

- 打招呼。
- 查询价格。
- 解析邮件。
- 生成报价。

当前阶段我们只做最简单的 `hello`。

它不访问数据库。

它不调用外部系统。

它只接收一个名字，然后返回问候语。

### 在本项目中的例子

当前项目的 Tool 是：

```python
hello(name: str) -> dict
```

它接收 `name`，返回结构化结果。

### 为什么重要

Tool 是 MCP 最核心的学习对象之一。

因为 AI 只有通过 Tool，才能从“只会生成文本”变成“可以调用受控能力”。

### 如何验证

运行：

```bash
uv run fastmcp list src/server.py
```

如果能看到 `hello(name: str) -> dict`，说明 Tool 已经暴露成功。

也可以运行：

```bash
uv run fastmcp call src/server.py hello name=Alice --json
```

如果返回 `Hello, Alice!`，说明 Tool 能被调用。

### 容易混淆的点

Tool 不是随便一个 Python 函数。

只有注册到 FastMCP Server 的函数，才是 MCP Tool。

## `@mcp.tool`

### 一句话理解

`@mcp.tool` 可以理解为“把普通 Python 函数登记成 MCP Tool 的标记”。

### 通俗解释

原本 `hello` 只是一个普通函数。

加上 `@mcp.tool` 以后，FastMCP 会把它登记到 Server 里。

登记后，Client 才能发现它、查看它的参数、调用它。

### 在本项目中的例子

```python
@mcp.tool
def hello(name: str) -> dict:
    ...
```

这表示：把 `hello` 注册成一个 MCP Tool。

### 为什么重要

它是从“普通 Python 代码”进入“MCP 世界”的入口。

这个装饰器让我们不用手写复杂协议注册代码。

### 如何验证

运行：

```bash
uv run fastmcp list src/server.py
```

如果 list 结果里能看到 `hello`，说明 `@mcp.tool` 起作用了。

### 容易混淆的点

`@mcp.tool` 不是启动 Server。

它只是注册 Tool。

真正启动 Server 的是：

```python
mcp.run(...)
```

## Tool 参数类型

### 一句话理解

Tool 参数类型可以理解为“告诉 Client 这个 Tool 需要什么输入”。

### 通俗解释

Python 里写：

```python
name: str
```

意思是 `name` 应该是字符串。

FastMCP 会读取这个类型信息。

然后它可以告诉 Client：调用 `hello` 时，需要传一个字符串类型的 `name`。

### 在本项目中的例子

`hello` 的参数是：

```python
name: str
```

所以调用时可以这样传：

```bash
uv run fastmcp call src/server.py hello name=Alice --json
```

### 为什么重要

类型越清楚，Client 越容易正确调用。

后续做报价 Demo 时，参数可能会变成邮件文本、商品名、数量等。

如果类型不清楚，Tool 很容易被错误调用。

### 如何验证

运行：

```bash
uv run fastmcp list src/server.py
```

看到：

```text
hello(name: str) -> dict
```

就说明类型信息已经被 FastMCP 识别到了。

### 容易混淆的点

类型注解不是业务校验的全部。

`name: str` 只能说明它应该是字符串。

但“不能为空”这种规则，仍然需要在函数里自己判断。

## Tool 结构化返回

### 一句话理解

Tool 结构化返回可以理解为“让结果像数据，而不是像一段话”。

### 通俗解释

如果 Tool 只返回：

```text
Hello, Alice!
```

人能看懂。

但程序很难稳定判断它是成功还是失败。

所以本项目统一返回：

```python
{"success": True, "data": {...}}
```

失败时返回：

```python
{"success": False, "error": "..."}
```

这样后续 Client 可以直接判断 `success`。

### 在本项目中的例子

正常输入：

```python
hello("Alice")
```

返回：

```python
{"success": True, "data": {"message": "Hello, Alice!"}}
```

空白输入：

```python
hello("   ")
```

返回：

```python
{"success": False, "error": "name is required"}
```

### 为什么重要

业务系统更需要稳定数据，而不是好看的自然语言。

后续 QuoteAgent 风格 Demo 需要返回商品、数量、单价、总价。

这些都适合结构化返回。

### 如何验证

运行：

```bash
uv run fastmcp call src/server.py hello name=Alice --json
uv run fastmcp call src/server.py hello name='   ' --json
```

查看 `structured_content` 中的 `success`、`data`、`error`。

### 容易混淆的点

结构化返回不代表不能给人看。

它只是优先保证程序好处理。

如果需要展示给人，可以让 Client 再把结构化数据转换成文字。

## HTTP Transport

### 一句话理解

HTTP Transport 可以理解为“让 MCP Server 通过本地 HTTP 地址对外服务”。

### 通俗解释

Server 写好后，需要一种通信方式让 Client 连上来。

这个通信方式就叫 Transport。

当前项目使用 HTTP。

启动后，Server 会监听：

```text
http://127.0.0.1:8000/mcp
```

后续 Client 可以通过这个地址调用 Server。

### 在本项目中的例子

`src/server.py` 中：

```python
mcp.run(transport="http", host="127.0.0.1", port=8000)
```

### 为什么重要

HTTP 模式更接近真实应用里的“服务调用”。

它也方便后续学习 Client 如何连接 Server。

### 如何验证

运行：

```bash
uv run python src/server.py
```

看到类似：

```text
Uvicorn running on http://127.0.0.1:8000
```

以及 MCP 入口 `/mcp`，说明 HTTP Server 已启动。

### 容易混淆的点

HTTP Transport 不等于普通 REST API。

虽然它用 HTTP 运行，但里面走的是 MCP 通信方式。

当前阶段不要把它设计成传统 Web Controller。

## MCP Client

### 一句话理解

MCP Client 可以理解为“连接 MCP Server，并调用它能力的一方”。

### 通俗解释

Server 负责提供能力。

Client 负责发现能力、选择能力、调用能力、读取结果。

在真实场景里，Client 可能是 AI 助手、桌面工具、IDE 插件，或者我们自己写的 Python Client。

当前项目还没有实现 `src/client.py`。

它会在后续 Step 2 中实现。

### 在本项目中的例子

现在的 `src/client.py` 仍然是占位文件。

但我们已经可以用 FastMCP CLI 先临时扮演 Client：

```bash
uv run fastmcp call src/server.py hello name=Alice --json
```

### 为什么重要

只写 Server 还不算完成闭环。

真正的 MCP 闭环是：

Client 发现 Server 的 Tool，然后调用 Tool，再处理返回结果。

### 如何验证

当前阶段可以用 CLI 验证调用。

后续实现 `src/client.py` 后，可以运行：

```bash
uv run python src/client.py
```

如果 Client 能调用 `hello` 并拿到结构化结果，说明闭环成立。

### 容易混淆的点

Client 不是 Tool。

Tool 是 Server 暴露出来的能力。

Client 是调用这些能力的一方。

## `fastmcp inspect`

### 一句话理解

`fastmcp inspect` 可以理解为“检查这个 Server 整体有没有被正确识别”。

### 通俗解释

它更像体检报告。

它关心的是：

- Server 叫什么。
- FastMCP 版本是什么。
- 有几个 Tool。
- 有几个 Resource。
- 有几个 Prompt。

它不重点展示每个 Tool 的详细用法。

### 在本项目中的例子

运行：

```bash
uv run fastmcp inspect src/server.py
```

当前会看到 Tools 数量为 1。

### 为什么重要

当 Server 加载失败、Tool 没注册上、组件数量不对时，先看 inspect 很有用。

它适合做第一层检查。

### 如何验证

确认输出里有：

```text
Name: fastmcp-learning-demo
Tools: 1
```

### 容易混淆的点

`inspect` 不是用来调用 Tool 的。

它是看 Server 的整体信息。

调用 Tool 要用 Client，或者临时用：

```bash
uv run fastmcp call ...
```

## `fastmcp list`

### 一句话理解

`fastmcp list` 可以理解为“列出这个 Server 现在有哪些 Tool 可用”。

### 通俗解释

它更像菜单。

你可以用它看：

- Tool 名字。
- Tool 参数。
- Tool 返回类型。
- Tool 的 docstring 说明。

### 在本项目中的例子

运行：

```bash
uv run fastmcp list src/server.py
```

当前会看到：

```text
hello(name: str) -> dict
```

以及 `hello` 的说明。

### 为什么重要

写完 Tool 后，不能只看代码。

还要确认它真的被 Server 暴露出来。

`fastmcp list` 就是做这个确认。

### 如何验证

确认输出里有：

```text
hello(name: str) -> dict
```

### 容易混淆的点

`list` 和 `inspect` 都会加载 Server。

但关注点不同。

`inspect` 看整体。

`list` 看 Tool 清单。

## Tools / Resources / Prompts 的区别

### 一句话理解

Tools 是“能做事”，Resources 是“能读取资料”，Prompts 是“提供提示模板”。

### 通俗解释

可以先这样记：

- Tool：动作。比如 `hello`、计算报价、解析邮件。
- Resource：资料。比如读取某个文件、配置、文档内容。
- Prompt：提示词模板。比如一段固定格式的任务说明。

它们都是 MCP Server 可以暴露的能力。

但用途不同。

### 在本项目中的例子

当前项目只实现了 Tool：

```text
hello(name: str) -> dict
```

还没有实现 Resource。

还没有实现 Prompt。

后续 QuoteAgent 风格 Demo 里：

- 解析报价邮件，适合做 Tool。
- 本地假价格表，如果只是读取资料，未来可以考虑 Resource。
- 固定报价分析说明，未来可以考虑 Prompt。

### 为什么重要

学 MCP 时很容易把所有东西都做成 Tool。

但 MCP 里不同能力有不同位置。

分清这三者，后续设计会更清楚。

### 如何验证

运行：

```bash
uv run fastmcp inspect src/server.py
```

当前应该看到：

```text
Tools: 1
Prompts: 0
Resources: 0
```

这说明本项目现在只暴露了 Tool。

### 容易混淆的点

Tool 和 Resource 最容易混。

简单区分：

- 需要执行动作，用 Tool。
- 只是提供内容，用 Resource。

Prompt 不是执行动作。

Prompt 更像给 AI 使用的一段可复用任务模板。

## 后续待补充

后续学习到新概念时，继续按这个结构补充：

1. 一句话理解。
2. 通俗解释。
3. 在本项目中的例子。
4. 为什么重要。
5. 如何验证。
6. 容易混淆的点。
