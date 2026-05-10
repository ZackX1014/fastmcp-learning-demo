# 007 Tool Resource Prompt Workflow

## 一句话理解

小型 Agent 工作流可以理解为“Client 按顺序把资料、指令和动作串起来”。

## 通俗解释

前几步我们分别学了三个东西。

Resource 像资料柜。

Prompt 像任务说明书。

Tool 像可以执行的动作。

Step 7 不是新增一个更复杂的能力。

它只是把前面学过的能力按顺序连起来。

流程是：

1. 先读取项目上下文。
2. 再获取报价分析 Prompt。
3. 最后调用报价计算 Tool。

当前没有真实 LLM。

所以 Prompt 只是被打印出来。

如果以后接入 LLM，下一步才会把 Prompt 和上下文交给 LLM 分析。

## 在本项目中的例子

`src/client_agent_workflow_demo.py` 做了三件事：

```python
await client.read_resource("project://summary")
```

读取项目摘要。

```python
await client.get_prompt("analyze_quote_request", {...})
```

获取报价分析提示模板。

```python
await client.call_tool("calculate_quote_price", {...})
```

调用报价计算 Tool。

这三个调用组成了一个最小的模拟 Agent 工作流。

## 为什么重要

真实 AI 业务系统通常不是只调用一个 Tool。

它往往需要：

- 先读取上下文。
- 再拿到稳定的指令模板。
- 再调用确定性的业务能力。
- 最后把结果整理出来。

Agent 通常可以理解为：

`LLM + Prompt + Resource + Tool + 控制流程`

当前项目还没有 LLM。

但 Step 7 已经把“控制流程”这个部分演示出来了。

## 如何验证

先启动 Server：

```bash
uv run python src/server.py
```

另开终端运行 Step 7 Demo：

```bash
uv run python src/client_agent_workflow_demo.py
```

输出中应该能看到：

- `Step 1: Loaded Resource`
- `Step 2: Loaded Prompt`
- `Step 3: Called Tool`
- `Final Simulated Agent Workflow Result`
- 报价计算结果中的 `total_price` 和 `currency`

也可以检查 Server 暴露的能力：

```bash
uv run fastmcp inspect src/server.py
```

应该能看到已有 Tool、Resource 和 Prompt。

## 容易混淆的点

### Agent 不是单个 Tool

Tool 只负责一个明确动作。

Agent 更像一个流程。

它会决定什么时候读资料、什么时候看提示、什么时候调用 Tool。

### Prompt 本身不执行逻辑

Prompt 是指令模板。

它不会自动分析报价需求。

它也不会自动计算价格。

需要 LLM 使用它，才会产生 AI 分析结果。

当前 Step 7 没有接入真实 LLM。

### Resource 不适合做业务动作

Resource 适合放上下文资料。

比如项目说明、规则说明、价格表。

如果要计算报价，应交给 Tool。

### Tool 更适合确定性业务动作

`calculate_quote_price` 有明确输入和明确输出。

同样参数会得到同样计算结果。

这类逻辑适合做成 Tool。

### Client / Workflow 负责串联

Server 暴露能力。

Client 使用能力。

Workflow 决定调用顺序。

这就是 Step 7 想练习的重点。
