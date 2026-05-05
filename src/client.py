"""Minimal FastMCP Client for calling the local hello tool."""

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"


def _to_json(value: Any) -> str:
    """Format values for readable console output."""
    return json.dumps(value, ensure_ascii=False, indent=2)


async def call_hello() -> None:
    """Connect to the local MCP Server and call the hello tool."""
    try:
        async with Client(SERVER_URL) as client:
            result = await client.call_tool("hello", {"name": "FastMCP"})
    except Exception as exc:
        print(f"Failed to call hello tool: {exc}")
        return

    print("hello tool result:")
    print(_to_json(result.structured_content))


def main() -> None:
    """Run the minimal MCP Client."""
    asyncio.run(call_hello())


if __name__ == "__main__":
    main()
