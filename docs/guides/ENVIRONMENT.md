# Environment

## 环境管理规则

- 本项目使用 uv 管理 Python 环境和依赖。
- Python 版本固定为 3.12。
- 依赖记录在 `pyproject.toml`。
- 依赖锁定在 `uv.lock`。
- 不使用系统 Python 全局安装依赖。
- 不使用全局 `pip install fastmcp`。
- 不创建 `requirements.txt`。
- 当前阶段不使用 Docker。
- 所有运行命令优先使用 `uv run`。

## 常用命令

```bash
uv init
uv python pin 3.12
uv add fastmcp
uv run fastmcp version
uv run python src/server.py
uv run python src/client.py
uv run fastmcp inspect src/server.py
uv run fastmcp list src/server.py
```

## 本机说明

如果 shell 中找不到 `uv`，可以使用本机路径：

```bash
/Users/xuqiang/.local/bin/uv
```

当前沙箱环境下可将 uv 缓存放在项目内：

```bash
UV_CACHE_DIR=.uv-cache uv run fastmcp version
```
