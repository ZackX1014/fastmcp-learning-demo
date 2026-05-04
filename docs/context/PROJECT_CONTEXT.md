# Project Context

## 项目目标

`fastmcp-learning-demo` 是一个独立 FastMCP 学习项目，用于快速理解 MCP Server、Tool、Client 的基本闭环。

## 当前阶段

当前处于 Step 0：初始化 uv 环境、目录结构、文档驱动开发结构和学习记录文档。

## 学习范围

- 创建 FastMCP Server。
- 暴露 MCP Tool。
- 使用 Client 调用 Tool。
- 使用 HTTP 运行。
- 使用 CLI inspect / list 检查。
- 完成 QuoteAgent 风格的本地模拟 Demo。

## 暂不包含范围

- 不接入真实 QuoteAgent 项目。
- 不调用 ASP.NET Core API。
- 不引入数据库。
- 不接入真实邮箱。
- 不实现认证授权。
- 不做部署配置。
- 不创建 Docker 配置。

## 最终 Demo 目标

输入报价邮件文本，解析商品和数量，根据本地假价格表计算报价，并返回结构化 JSON。

## 与 QuoteAgent 的关系

本项目只做 QuoteAgent 风格模拟，用于学习 MCP Tool 的业务建模方式，不直接集成或依赖真实 QuoteAgent 项目。
