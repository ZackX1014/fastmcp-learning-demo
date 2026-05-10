# 008 QuoteAgent Simulation Workflow

## 一句话理解

QuoteAgent 风格流程可以理解为“先判断信息够不够，再决定要不要调用报价 Tool”。

## 通俗解释

Step 7 已经把 Resource、Prompt、Tool 串起来了。

Step 8 又往前走了一小步。

它多了一个业务判断：

这条报价请求的信息够不够？

如果信息完整，就调用 `calculate_quote_price`。

如果信息不完整，就先告诉用户缺什么。

当前判断不是 LLM 做的。

它只是本地简单规则。

这样更适合学习，因为每一步都看得见。

## 在本项目中的例子

`src/client_quote_agent_simulation_demo.py` 准备了两个 Case。

完整请求：

```text
Customer wants 10 standard sensors for JP region with urgent delivery.
```

不完整请求：

```text
Customer wants standard sensors for JP region.
```

完整请求会解析出：

```python
{
    "product_type": "standard_sensor",
    "quantity": 10,
    "region": "JP",
    "urgency": "urgent",
}
```

然后调用：

```python
await client.call_tool("calculate_quote_price", extracted)
```

不完整请求缺少：

```python
["quantity", "urgency"]
```

所以不会调用报价 Tool。

## 为什么重要

真实 Agent 不只是会调用 Tool。

它还要判断什么时候可以调用 Tool。

如果信息不完整还硬调用 Tool，就可能得到错误结果。

比如报价请求没有数量。

这时最合理的动作不是计算价格。

而是先问清楚数量。

这就是业务流程控制。

## 如何验证

先启动 Server：

```bash
uv run python src/server.py
```

另开终端运行 Step 8 Demo：

```bash
uv run python src/client_quote_agent_simulation_demo.py
```

输出中应该能看到：

- `Complete request case`
- `Incomplete request case`
- 完整请求调用了 `calculate_quote_price`
- 不完整请求没有调用 Tool
- 不完整请求输出了 `missing_fields`

## 容易混淆的点

### Step 8 和 Step 7 的区别

Step 7 只是把 Resource、Prompt、Tool 串起来。

Step 8 多了业务判断。

它会根据请求是否完整，决定下一步做什么。

### Prompt 本身不等于 LLM

Prompt 是分析指令模板。

它告诉 AI 应该怎么分析。

但本 Demo 没有真实 LLM。

所以完整性判断由本地函数模拟。

### Resource 不会自动做决定

Resource 只提供上下文资料。

它不会判断报价请求是否完整。

它也不会调用 Tool。

### Tool 应该保持确定性

`calculate_quote_price` 只负责计算报价。

它不负责理解整封邮件。

它不负责追问用户。

这样 Tool 的职责更清楚。

### 信息不完整时不要硬调用 Tool

缺少数量或紧急程度时，调用报价 Tool 没有意义。

更好的流程是返回 `missing_fields`。

然后让用户补充信息。

这更接近真实业务 Agent 的工作方式。
