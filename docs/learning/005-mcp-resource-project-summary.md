# 005 MCP Resource Project Summary

## 一句话理解

Resource 可以理解为“让 Client 读取资料的入口”。

## 通俗解释

前几步我们一直在学习 Tool。

Tool 更像动作。

比如：

- 打招呼。
- 计算报价。
- 校验参数。

Resource 不强调执行动作。

它更像资料。

比如：

- 项目说明。
- 价格表。
- 业务规则。
- 文档内容。

Step 5 新增的 `project://summary` 就是一个只读资料入口。

Client 读取它时，Server 返回当前学习项目的摘要。

## 在本项目中的例子

Server 注册 Resource：

```python
@mcp.resource("project://summary")
def get_project_summary() -> dict:
    ...
```

Client 读取 Resource：

```python
contents = await client.read_resource("project://summary")
```

Resource 返回的信息包括：

- `project_name`
- `project_type`
- `goal`
- `completed_steps`
- `current_focus`
- `note`

## 为什么重要

AI 业务系统不只需要“能做事”的 Tool。

它也需要“能读取背景资料”的 Resource。

比如未来 QuoteAgent 风格 Demo 里，Resource 可以用来提供：

- 项目上下文。
- 本地假价格表。
- 报价规则说明。
- 学习阶段说明。

这些资料不一定要触发业务动作。

它们更适合被读取。

## 如何验证

先检查 Server：

```bash
uv run fastmcp inspect src/server.py
```

应该能看到 Resource 数量变为 1。

然后启动 Server：

```bash
uv run python src/server.py
```

另开终端运行 Resource Demo：

```bash
uv run python src/client_resource_demo.py
```

输出中应该能看到：

- `project_name`
- `goal`
- `completed_steps`
- `current_focus`

## 容易混淆的点

### Tool 和 Resource 的区别

Tool 更像“执行动作”。

Resource 更像“读取资料”。

`calculate_quote_price` 是 Tool，因为它根据输入计算报价。

`project://summary` 是 Resource，因为它只是返回项目摘要。

### Resource 为什么应该只读

Resource 的直觉是“读取资料”。

如果读取 Resource 时还修改数据，调用方会很难理解它的副作用。

本项目的 `project://summary` 不写文件、不改状态、不访问数据库。

它只返回固定项目说明。

### 读取 Resource 和调用 Tool 的区别

调用 Tool：

```python
await client.call_tool("calculate_quote_price", {...})
```

读取 Resource：

```python
await client.read_resource("project://summary")
```

一个是执行动作。

一个是读取资料。

### 和未来业务系统的关系

未来如果做更像 AI 业务系统的 Demo，Resource 可以承担“上下文资料”的角色。

比如：

- 知识库内容。
- 项目规则。
- 业务说明。
- 本地假价格表。

这样 Tool 负责做事，Resource 负责提供背景资料。
