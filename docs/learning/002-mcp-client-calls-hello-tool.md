# 002 MCP Client Calls Hello Tool

## 这一步学什么

这一步学习 MCP Client。

我们让 `src/client.py` 连接本地 FastMCP Server。

然后调用 Step 1 里实现的 `hello` Tool。

这一步完成最小 MCP 调用闭环：

```text
Client -> Server -> Tool -> Result -> Client
```

## MCP Client

一句话理解：

MCP Client 可以理解为“连接 Server，并使用 Server 能力的一方”。

Server 负责暴露能力。

Client 负责使用能力。

当前项目里，Client 做的事很少：

1. 连接 `http://127.0.0.1:8000/mcp`。
2. 调用 `hello`。
3. 传入 `{"name": "FastMCP"}`。
4. 打印返回结果。

## Client 和 Server 的关系

可以把它们理解成：

- Server：能力提供方。
- Client：能力调用方。

调用过程是：

1. Server 先启动。
2. Client 连接 Server 地址。
3. Client 告诉 Server 要调用哪个 Tool。
4. Server 执行 Tool。
5. Server 把结果返回给 Client。

这个关系后续不会变。

无论是 `hello`，还是后面的报价 Tool，本质都是这个流程。

## HTTP Transport

Transport 可以理解为“通信通道”。

Server 使用 HTTP 模式启动：

```python
mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Client 连接的地址是：

```python
Client("http://127.0.0.1:8000/mcp")
```

两边要对应。

如果 Server 没启动，或者地址写错，Client 就无法调用 Tool。

注意：

HTTP Transport 不等于普通 REST API。

它底层用 HTTP，但传的是 MCP 协议消息。

## Client 如何调用 Tool

调用 Tool 需要两个东西：

- Tool 名称。
- Tool 参数。

在本项目里：

```python
await client.call_tool("hello", {"name": "FastMCP"})
```

`hello` 是 Tool 名称。

`{"name": "FastMCP"}` 是传给 Tool 的参数。

Server 收到请求后，会执行 `hello(name="FastMCP")`。

然后把结构化结果返回给 Client。

## Tool 调用结果

FastMCP Client 返回的是调用结果对象。

本项目里我们重点看：

```python
result.structured_content
```

它包含 Tool 返回的结构化数据。

预期类似：

```python
{
    "success": True,
    "data": {
        "message": "Hello, FastMCP!"
    },
}
```

## 在本项目中的例子

`src/client.py` 的核心代码：

```python
async with Client(SERVER_URL) as client:
    result = await client.call_tool("hello", {"name": "FastMCP"})
    print(result.structured_content)
```

这里用了 `async with`。

可以简单理解为：

进入代码块时连接 Server。

离开代码块时关闭连接。

## 如何验证

先启动 Server：

```bash
uv run python src/server.py
```

另开一个终端运行 Client：

```bash
uv run python src/client.py
```

预期：

- Client 能连接本地 Server。
- `hello` Tool 调用成功。
- 输出里能看到 `Hello, FastMCP!`。

## 和传统 Web 调用的对比

相似点：

- 都有服务端和调用方。
- 都需要地址。
- 都会传参数并拿结果。

不同点：

- 传统 Web API 常调用 HTTP 路由，比如 `/api/quotes`。
- MCP Client 调用的是 Tool 名称，比如 `hello`。
- MCP Server 暴露的不只是 Tool，后续还可以暴露 Resource 和 Prompt。

## 容易混淆的点

- Client 不是 Tool，Client 是调用方。
- Server 通常不会主动调用 Client。
- `call_tool` 会实际执行 Tool。
- `inspect` / `list` 只是检查能力，不会执行业务逻辑。
- Step 2 的重点是调用闭环，不是报价业务。
