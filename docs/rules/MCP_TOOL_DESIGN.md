# MCP Tool Design

## Tool 设计规则

- Tool 代表清晰业务动作。
- Tool 名称使用 snake_case，动词开头。
- Tool 必须有 docstring。
- Tool 参数必须有明确类型。
- Tool 返回结构化 `dict`。
- 成功返回：

```python
{"success": True, "data": ...}
```

- 失败返回：

```python
{"success": False, "error": "..."}
```

- 当前阶段不调用真实外部系统。
- 当前阶段使用本地假数据。
