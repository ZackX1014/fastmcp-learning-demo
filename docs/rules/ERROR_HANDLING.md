# Error Handling

## 错误处理规则

- 当前阶段不设计复杂异常体系。
- 成功返回结构：

```python
{"success": True, "data": ...}
```

- 失败返回结构：

```python
{"success": False, "error": "..."}
```

- `warnings` 和 `errors` 要区分。
- `error` 表示无法继续执行。
- `warning` 表示可以返回结果，但信息不完整。
- 不要把未处理异常直接暴露给 Client。
