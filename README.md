# fastmcp-learning-demo

## 项目目标

本项目是一个独立的 FastMCP 学习 Demo，用于在两天内快速掌握 MCP Server、Tool、Client、HTTP 运行方式和 CLI 检查工具的基本闭环。

最终会实现一个 QuoteAgent 风格的模拟 Demo：输入报价邮件文本，解析商品和数量，根据本地假价格表计算报价，并返回结构化 JSON。

## 当前阶段范围

当前阶段只完成环境初始化、目录结构、文档结构和最小占位代码文件。

## 暂不包含内容

- 不接入真实 QuoteAgent 项目。
- 不调用 ASP.NET Core API。
- 不引入数据库。
- 不接入真实邮箱。
- 不实现认证授权。
- 不做部署配置。
- 不创建 Docker 配置。
- 不创建 `requirements.txt`。
- 不实现 FastMCP Server 业务代码。

## 两天学习路线

第一天：

1. 初始化 uv 环境和文档驱动项目结构。
2. 创建最小 FastMCP Server。
3. 暴露第一个 MCP Tool。
4. 使用 CLI inspect / list 检查 Tool。
5. 使用 Client 调用 Tool。

第二天：

1. 使用 HTTP Transport 运行 Server。
2. 设计结构化 Tool 输入和输出。
3. 完成 QuoteAgent 风格的本地模拟报价 Tool。
4. 补充错误处理和验证记录。
5. 汇总核心概念和复盘学习路径。

## 环境管理方式

本项目使用 uv 管理 Python 版本、虚拟环境和依赖。

- Python 版本固定为 3.12。
- 依赖记录在 `pyproject.toml`。
- 依赖版本锁定在 `uv.lock`。
- 所有运行命令优先使用 `uv run`。

## 文档驱动开发方式

每次开发前先阅读 `AGENTS.md` 指定的上下文、规则、指南和学习记录。每次开发后更新 `docs/logs/DEV_LOG.md`，必要时更新 `docs/learning/CORE_CONCEPTS.md`。

## 学习记录方式

- `docs/logs/DEV_LOG.md` 记录每一步做了什么、如何验证、结果如何、下一步是什么。
- `docs/learning/CORE_CONCEPTS.md` 记录可复用的核心概念、原理和验证方式。

## 常用命令占位

```bash
uv run fastmcp version
uv run python src/server.py
uv run python src/client.py
uv run fastmcp inspect src/server.py
uv run fastmcp list src/server.py
```

## 后续验证方式占位

后续每完成一个 Tool 或 Client 步骤，都需要记录正常输入、空输入、非法输入和未识别商品等验证结果。
