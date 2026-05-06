"""FastMCP learning demo client."""

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"


def _to_json(value: Any) -> str:
    """Format values for readable console output."""
    return json.dumps(value, ensure_ascii=False, indent=2)


async def call_hello(client: Client) -> None:
    """Call the hello tool and print its structured result."""
    result = await client.call_tool("hello", {"name": "FastMCP"})
    print("hello tool result:")
    print(_to_json(result.structured_content))


async def call_calculate_quote_price(client: Client) -> None:
    """Call the quote price calculator tool and print its structured result."""
    result = await client.call_tool(
        "calculate_quote_price",
        {
            "product_type": "premium",
            "quantity": 3,
            "region": "JP",
            "urgency": "urgent",
        },
    )
    print("calculate_quote_price tool result:")
    print(_to_json(result.structured_content))


async def run_client() -> None:
    """Connect to the local MCP Server and call demo tools."""
    try:
        async with Client(SERVER_URL) as client:
            await call_hello(client)
            await call_calculate_quote_price(client)
    except Exception as exc:
        print(f"Failed to call MCP tools: {exc}")


def main() -> None:
    """Run the minimal MCP Client."""
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
