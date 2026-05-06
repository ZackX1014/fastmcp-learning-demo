# Testing

## 验证 FastMCP 已安装

```bash
uv run fastmcp version
```

如果能输出 FastMCP 版本号，说明依赖已安装且 uv 环境可用。

## 启动 Server

```bash
uv run python src/server.py
```

当前阶段 `src/server.py` 只是占位文件，后续实现 Server 后再补充实际启动结果。

## 运行 Client

```bash
uv run python src/client.py
```

当前阶段 `src/client.py` 只是占位文件，后续实现 Client 后再补充实际调用结果。

## 使用 fastmcp inspect

```bash
uv run fastmcp inspect src/server.py
```

用于检查 Server 和 Tool 的元数据。当前阶段暂未实现 Server，后续实现后再使用。

## 使用 fastmcp list

```bash
uv run fastmcp list src/server.py
```

用于列出 Server 暴露的 Tool。当前阶段暂未实现 Tool，后续实现后再使用。

## 每个 Tool 需要验证

- 正常输入。
- 空输入。
- 非法输入。
- 未识别商品。

## 每次完成后需要说明

- 修改内容。
- 验证方式。
- 验证结果。
- 是否建议提交 Git。

## Step 4：验证 Tool 输入校验和错误调用

### 启动 Server

```bash
uv run python src/server.py
```

期望：

- Server 正常启动。
- 地址仍然是 `http://127.0.0.1:8000/mcp`。

### 运行正常 Client

```bash
uv run python src/client.py
```

期望：

- `hello` Tool 正常。
- `calculate_quote_price` Tool 正常。
- 能看到 `total_price` 等结构化字段。

### 运行错误调用 Demo

```bash
uv run python src/client_error_demo.py
```

期望：

- 三个错误场景都被执行。
- 每个错误场景都能看到对应错误信息。
- 程序不会在第一个错误后直接退出。

## Step 5：验证 MCP Resource

### 启动 Server

```bash
uv run python src/server.py
```

期望：

- Server 正常启动。
- 地址仍然是 `http://127.0.0.1:8000/mcp`。

### 检查 Resource 是否能被识别

```bash
uv run fastmcp inspect src/server.py
```

期望：

- 能看到已有 Tools。
- 能看到新增 Resource `project://summary`。

### 运行 Resource Client Demo

```bash
uv run python src/client_resource_demo.py
```

期望：

- 能成功读取 `project://summary`。
- 输出中能看到 `project_name`、`goal`、`completed_steps`、`current_focus` 等信息。
