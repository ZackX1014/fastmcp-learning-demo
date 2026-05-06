# 004 Tool Validation And Error Handling

## 一句话理解

Tool 不只要会处理正确输入，也要能清楚处理错误输入。

## 通俗解释

Step 3 的 `calculate_quote_price` 已经能计算正常报价。

Step 4 关注另一半：输入不合法时怎么办。

比如：

- 数量是 0。
- 商品类型是空字符串。
- 加急状态传了 `rush`。

这些都不是系统崩溃。

它们是业务 Tool 应该能识别并返回清晰错误的情况。

## 在本项目中的例子

`calculate_quote_price` 会检查：

- `product_type` 不能为空。
- `quantity` 必须大于 0。
- `region` 不能为空。
- `urgency` 只能是 `normal` 或 `urgent`。

错误调用 Demo 放在：

```text
src/client_error_demo.py
```

它会分别调用三个错误场景，并打印每次返回的结构化结果。

## 为什么重要

业务型 Tool 不能只考虑成功路径。

真实业务里，输入经常不完整或不符合规则。

如果 Tool 没有清楚的输入校验，Client 就很难判断下一步该怎么办。

结构化错误结果可以让调用方稳定读取：

```python
{"success": False, "error": "..."}
```

这比让异常直接暴露给 Client 更适合学习和业务流程控制。

## 如何验证

先启动 Server：

```bash
uv run python src/server.py
```

确认正常 Client 没被破坏：

```bash
uv run python src/client.py
```

再运行错误调用 Demo：

```bash
uv run python src/client_error_demo.py
```

应该能看到三个场景都执行完：

- `quantity = 0`
- `product_type` 为空字符串
- `urgency = rush`

每个场景都应该看到 `success: false` 和对应的 `error`。

## 容易混淆的点

### Tool 参数错误和业务规则错误

Tool 参数错误偏向“调用形状不对”。

比如少传字段、类型完全不对。

业务规则错误偏向“字段有值，但不符合业务规则”。

比如 `quantity = 0`，它是整数，但报价数量不能为 0。

### 业务错误不一定要抛异常

本项目里，业务错误返回：

```python
{"success": False, "error": "..."}
```

这样 Client 可以继续运行，观察所有错误场景。

### 错误 Demo 不应该混在正常 client.py 里

`src/client.py` 用来展示正常调用路径。

`src/client_error_demo.py` 专门展示错误边界。

分开以后，复习时更清楚：

- 正常路径看 `client.py`。
- 错误路径看 `client_error_demo.py`。

### 和未来 QuoteAgent / 记账 App 的关系

未来如果做 QuoteAgent 风格 Demo，邮件可能缺商品、数量可能不合法、商品可能无法识别。

如果做记账 App，金额可能小于等于 0，分类可能为空。

这些都属于业务系统必须面对的错误边界。

所以错误场景不是附加内容，而是 Tool 设计的一部分。
