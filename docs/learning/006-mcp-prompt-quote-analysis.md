# 006 MCP Prompt Quote Analysis

## 一句话理解

Prompt 可以理解为“给 AI 使用的可复用指令模板”。

## 通俗解释

前面我们已经学了 Tool 和 Resource。

Tool 更像执行动作。

Resource 更像读取资料。

Prompt 更像一段可以复用的任务说明。

它告诉 AI 应该怎么分析问题。

但 Prompt 本身不等于 AI。

它也不会自己执行业务动作。

Step 6 新增的 `analyze_quote_request` 用来生成一段报价需求分析指令。

它不会计算价格。

它不会调用 `calculate_quote_price`。

它不会连接真实 LLM。

它只是返回一段清晰的分析模板。

## 在本项目中的例子

Server 注册 Prompt：

```python
@mcp.prompt(name="analyze_quote_request")
def analyze_quote_request(requirement_text: str, customer_region: str = "JP") -> str:
    ...
```

Client 获取 Prompt：

```python
prompt = await client.get_prompt(
    "analyze_quote_request",
    {
        "requirement_text": "We need 3 premium devices for our Tokyo office as soon as possible.",
        "customer_region": "JP",
    },
)
```

输出里会看到：

- 报价需求分析助手的角色说明。
- 要识别商品类型、数量、地区、紧急程度。
- 信息缺失时要列出确认问题。
- 不要编造缺失信息。
- 不要直接计算价格。

## 为什么重要

AI 业务系统经常需要稳定的指令模板。

如果每次都临时手写提示词，行为会很难保持一致。

Prompt 可以把“怎么分析”沉淀下来。

比如未来 QuoteAgent 风格 Demo 中：

- Prompt 负责指导 AI 如何分析报价邮件。
- Resource 可以提供上下文资料或规则。
- Tool 负责执行计算、解析或其他动作。

## 如何验证

先检查 Server：

```bash
uv run fastmcp inspect src/server.py
```

应该能看到 Prompt 数量变为 1。

然后启动 Server：

```bash
uv run python src/server.py
```

另开终端运行 Prompt Demo：

```bash
uv run python src/client_prompt_demo.py
```

输出中应该能看到：

- `analyze_quote_request`
- 示例 `requirement_text`
- `customer_region` 为 `JP`
- 报价需求分析相关指令

## 容易混淆的点

### Tool、Resource、Prompt 的区别

Tool 更像“执行动作”。

Resource 更像“读取资料”。

Prompt 更像“可复用的 AI 指令模板”。

### Prompt 本身不等于 LLM

Prompt 只是一段指令内容。

它不会自己生成智能结果。

要让 Prompt 产生 AI 分析结果，还需要真实 LLM 或 AI Client 使用它。

当前项目不接真实 LLM。

### Prompt 本身不直接执行业务动作

`analyze_quote_request` 不计算价格。

它也不调用 `calculate_quote_price`。

它只是告诉 AI 应该如何分析报价需求。

### 获取 Prompt 和调用 Tool 的区别

调用 Tool：

```python
await client.call_tool("calculate_quote_price", {...})
```

获取 Prompt：

```python
await client.get_prompt("analyze_quote_request", {...})
```

一个是执行动作。

一个是取回指令模板。

### 和未来 QuoteAgent 的关系

当前 Prompt 只是 QuoteAgent 风格模拟。

它模拟的是“报价需求分析提示模板”。

它不接真实 QuoteAgent。

不读取真实邮箱。

不调用 ASP.NET Core API。
