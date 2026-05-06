# 003 Quote Price Calculator Tool

## 一句话理解

`calculate_quote_price` 可以理解为“一个带业务参数和校验规则的报价计算 Tool”。

## 通俗解释

前面的 `hello` Tool 只负责打招呼。

它只有一个简单参数 `name`。

Step 3 的 `calculate_quote_price` 更接近业务系统里的能力。

它需要知道：

- 商品类型。
- 数量。
- 地区。
- 是否加急。

然后它根据本地假价格规则算出报价。

这个 Tool 不接数据库。

不接真实 QuoteAgent。

不调用外部 API。

它只是用简单规则模拟“报价计算”这个业务动作。

## 在本项目中的例子

Server 暴露的 Tool 是：

```python
calculate_quote_price(
    product_type: str,
    quantity: int,
    region: str = "JP",
    urgency: str = "normal",
) -> dict
```

Client 调用时传入：

```python
{
    "product_type": "premium",
    "quantity": 3,
    "region": "JP",
    "urgency": "urgent",
}
```

期望返回：

```json
{
  "success": true,
  "data": {
    "product_type": "premium",
    "quantity": 3,
    "region": "JP",
    "urgency": "urgent",
    "unit_price": 200,
    "subtotal": 600,
    "urgency_fee": 120,
    "total_price": 720,
    "currency": "JPY"
  }
}
```

## 为什么重要

这是从“演示型 Tool”走向“业务型 Tool”的第一步。

业务型 Tool 不只是能被调用。

它还要关注：

- 参数是否清楚。
- 输入是否合法。
- 返回值是否稳定。
- Client 是否容易读取结果。

后续 QuoteAgent 风格 Demo 会继续沿用这个思路。

## 如何验证

先检查 Server 暴露了哪些 Tool：

```bash
uv run fastmcp inspect src/server.py
uv run fastmcp list src/server.py
```

应该能看到：

- `hello`
- `calculate_quote_price`

然后启动 Server：

```bash
uv run python src/server.py
```

另开终端运行 Client：

```bash
uv run python src/client.py
```

输出中应该能看到：

- `product_type`
- `quantity`
- `unit_price`
- `subtotal`
- `urgency_fee`
- `total_price`
- `currency`

## 容易混淆的点

### 业务型 Tool 和 hello tool 的区别

`hello` 主要用于确认 Tool 注册和调用链路。

`calculate_quote_price` 开始模拟真实业务动作。

它有更多参数，也有更明确的业务规则。

### Tool 参数为什么要设计清楚

Client 调用 Tool 时，需要知道传什么。

参数越清楚，调用越稳定。

比如 `quantity: int` 就比随便传一个字符串更适合计算报价。

### 输入校验为什么重要

Tool 不能默认相信输入一定正确。

比如：

- 商品类型不能为空。
- 数量必须大于 0。
- 地区不能为空。
- 加急状态只能是 `normal` 或 `urgent`。

这些校验能让错误更早暴露，也让 Client 更容易处理失败。

### 结构化返回为什么重要

报价结果不是一句话。

它包含单价、小计、加急费、总价、币种。

这些字段应该稳定返回，方便 Client 或后续流程继续使用。

### Client 如何调用不同 Tool

Client 调用不同 Tool，本质上是换 Tool 名称和参数。

调用 `hello`：

```python
await client.call_tool("hello", {"name": "FastMCP"})
```

调用报价 Tool：

```python
await client.call_tool("calculate_quote_price", {...})
```

### 和未来 QuoteAgent 的关系

当前 Tool 只是 QuoteAgent 风格模拟。

它模拟的是“根据输入计算报价”的业务能力。

它不接真实 QuoteAgent 项目。

不读取真实邮件。

不访问真实价格表。

不调用 ASP.NET Core API。
