# 002 MCP Client Calls Hello Tool

## 这一步学什么

这一步学习 MCP Client。

我们让 `src/client.py` 连接本地 FastMCP Server。

然后调用 Step 1 里实现的 `hello` Tool。

这一步完成了最小 MCP 闭环：

```text
Client -> Server -> Tool -> Result -> Client
```

## 复习顺序

建议按这个顺序看：

1. MCP Client 是什么
2. Client 和 Server 的关系
3. HTTP Transport 在 Client 调用中的作用
4. Client 如何调用 Tool
5. Tool 调用结果如何返回
6. MCP 调用模型和传统前后端调用模型的相似点
7. MCP 调用模型和传统前后端调用模型的不同点

## MCP Client 是什么

### 一句话理解

MCP Client 可以理解为“连接 Server，并调用 Tool 的一方”。

### 通俗解释

Server 提供能力。

Client 使用能力。

在 MCP 里，Client 会连接到 Server，发现或调用 Server 暴露出来的 Tool。

当前项目里，Client 的任务很简单：

- 连接 `http://127.0.0.1:8000/mcp`
- 调用 `hello`
- 传入 `name = "FastMCP"`
- 打印返回结果

### 在本项目中的例子

`src/client.py` 使用：

```python
Client("http://127.0.0.1:8000/mcp")
```

这表示创建一个连接本地 FastMCP Server 的 Client。

### 为什么重要

只有 Server 还不算完成 MCP 学习闭环。

Client 能调用 Tool，才说明 Server 暴露的能力真的可以被外部使用。

### 如何验证

先启动 Server：

```bash
uv run python src/server.py
```

再运行 Client：

```bash
uv run python src/client.py
```

如果看到 `Hello, FastMCP!`，说明 Client 调用成功。

### 容易混淆的点

Client 不是 Tool。

Client 是调用方。

Tool 是 Server 暴露出来的能力。

## Client 和 Server 的关系

### 一句话理解

Client 可以理解为“请求方”，Server 可以理解为“能力提供方”。

### 通俗解释

Server 先启动。

Server 监听一个地址。

Client 再连接这个地址，并告诉 Server：我要调用哪个 Tool，参数是什么。

Server 收到请求后，执行对应 Tool，再把结果返回给 Client。

### 在本项目中的例子

Server 地址是：

```text
http://127.0.0.1:8000/mcp
```

Client 调用的是：

```text
hello
```

传入参数是：

```python
{"name": "FastMCP"}
```

### 为什么重要

这个关系是理解 MCP 的基础。

后续报价 Demo 也是一样：

Client 传入报价邮件文本。

Server 执行报价 Tool。

Client 拿到结构化报价结果。

### 如何验证

运行 Client 后，Server 终端会出现访问 `/mcp` 的请求日志。

Client 终端会打印 Tool 返回结果。

### 容易混淆的点

Server 不是主动调用 Client。

通常是 Client 主动连接 Server，并发起 Tool 调用。

## HTTP Transport 在 Client 调用中的作用

### 一句话理解

HTTP Transport 可以理解为“Client 和 Server 之间通话的通道”。

### 通俗解释

Transport 是通信方式。

当前项目使用 HTTP。

所以 Client 连接的是一个 HTTP 地址：

```text
http://127.0.0.1:8000/mcp
```

这个地址不是普通网页。

它是 FastMCP Server 暴露的 MCP 通信入口。

### 在本项目中的例子

Server 里使用：

```python
mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Client 里连接：

```python
Client("http://127.0.0.1:8000/mcp")
```

这两个地址要对应起来。

### 为什么重要

如果地址不对，Client 就连不上 Server。

如果 Server 没启动，Client 也无法调用 Tool。

### 如何验证

先启动 Server。

再运行 Client。

如果 Client 输出连接失败，优先检查：

- Server 是否正在运行。
- 地址是否是 `http://127.0.0.1:8000/mcp`。
- 端口是否被占用或被沙箱限制。

### 容易混淆的点

HTTP Transport 不等于 REST API。

它底层用 HTTP，但传的是 MCP 协议消息。

## Client 如何调用 Tool

### 一句话理解

Client 调用 Tool，可以理解为“告诉 Server：请执行这个名字的能力，并传入这些参数”。

### 通俗解释

调用 Tool 时，需要两个关键信息：

- Tool 名称。
- Tool 参数。

本项目中 Tool 名称是 `hello`。

参数是：

```python
{"name": "FastMCP"}
```

### 在本项目中的例子

`src/client.py` 中调用：

```python
await client.call_tool("hello", {"name": "FastMCP"})
```

这会让 Server 执行 `hello` Tool。

### 为什么重要

这是 MCP 最核心的动作。

后续所有业务 Demo，本质上都是换一个 Tool 名称和参数。

### 如何验证

运行：

```bash
uv run python src/client.py
```

看到：

```text
Hello, FastMCP!
```

说明 Tool 被调用成功。

### 容易混淆的点

Client 不是直接 import Server 的 Python 函数。

Client 是通过 MCP 协议请求 Server 执行 Tool。

## Tool 调用结果如何返回

### 一句话理解

Tool 调用结果可以理解为“Server 执行完 Tool 后返回给 Client 的结构化数据”。

### 通俗解释

`hello` Tool 返回的是一个 `dict`。

FastMCP 会把这个结果通过 MCP 响应返回给 Client。

Client 再从结果里读取结构化内容，并打印出来。

### 在本项目中的例子

Client 打印结果：

```json
{
  "success": true,
  "data": {
    "message": "Hello, FastMCP!"
  }
}
```

### 为什么重要

业务系统不能只靠自然语言。

结构化结果更容易被后续代码判断和复用。

比如后续报价 Demo 可以读取：

- 商品名。
- 数量。
- 单价。
- 总价。
- 错误信息。

### 如何验证

运行 Client 后，确认输出中有：

```text
"success": true
"message": "Hello, FastMCP!"
```

### 容易混淆的点

Tool 返回里的 `success` 是业务层成功标记。

MCP 协议本身也有调用是否出错的状态。

当前 `hello` Tool 的返回结构是我们项目自己的约定。

## MCP 调用模型和传统前后端调用模型的相似点

### 一句话理解

MCP Client 调 Server，很像前端调后端。

### 通俗解释

传统 Web 系统里：

```text
Frontend -> Backend API -> Business Logic -> JSON Result
```

MCP 里可以先这样类比：

```text
MCP Client -> MCP Server -> Tool -> Structured Result
```

两者都有：

- 调用方。
- 服务方。
- 参数。
- 执行逻辑。
- 返回结果。

### 在本项目中的例子

`src/client.py` 类似一个很小的前端调用层。

`src/server.py` 类似一个后端能力容器。

`hello` 类似一个后端业务动作。

### 为什么重要

这个类比能降低学习门槛。

如果已经理解前端调用 API，就更容易理解 Client 调用 Tool。

### 如何验证

启动 Server，再运行 Client。

观察结果从 Server 返回到 Client。

### 容易混淆的点

这个类比只是帮助理解。

MCP 不是普通前后端框架。

## MCP 调用模型和传统前后端调用模型的不同点

### 一句话理解

MCP 更关注“给 AI 暴露能力”，传统 Web API 更关注“给应用暴露接口”。

### 通俗解释

传统 Web API 通常围绕 URL 和资源设计。

比如：

```text
GET /products
POST /orders
```

MCP 更关注 Tool、Resource、Prompt。

Client 关心的是：

- 有哪些 Tool。
- Tool 需要什么参数。
- Tool 返回什么结构。
- AI 或调用方能不能安全地使用这些能力。

### 在本项目中的例子

我们没有创建 `/hello` 路由。

我们创建的是 `hello` Tool。

Client 不是访问 `/hello`。

Client 是连接 `/mcp`，再通过 MCP 协议调用 `hello`。

### 为什么重要

如果把 MCP 完全当成 REST API，很容易设计跑偏。

MCP 的重点是能力发现和 Tool 调用，而不是手写一堆 HTTP 路由。

### 如何验证

运行：

```bash
uv run fastmcp list src/server.py
```

如果看到 `hello(name: str) -> dict`，说明它是 MCP Tool，而不是普通 HTTP 路由。

### 容易混淆的点

`http://127.0.0.1:8000/mcp` 是 MCP 入口。

它不是 `hello` Tool 的专属 URL。

Tool 调用发生在 MCP 协议消息里。
