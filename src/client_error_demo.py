"""Error scenario demo for the calculate_quote_price tool."""

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"


def _to_json(value: Any) -> str:
    """Format values for readable console output."""
    return json.dumps(value, ensure_ascii=False, indent=2)


async def run_error_case(
    client: Client,
    title: str,
    arguments: dict[str, Any],
) -> None:
    """Call calculate_quote_price with invalid arguments and print the result."""
    print(f"\n{title}")
    print("arguments:")
    print(_to_json(arguments))

    try:
        result = await client.call_tool("calculate_quote_price", arguments)
    except Exception as exc:
        print(f"call failed with exception: {exc}")
        return

    print("structured result:")
    print(_to_json(result.structured_content))


async def run_client() -> None:
    """Run all error scenarios without stopping after the first failure."""
    scenarios = [
        (
            "Scenario 1: quantity = 0",
            {
                "product_type": "premium",
                "quantity": 0,
                "region": "JP",
                "urgency": "normal",
            },
        ),
        (
            "Scenario 2: product_type is empty",
            {
                "product_type": "",
                "quantity": 3,
                "region": "JP",
                "urgency": "normal",
            },
        ),
        (
            "Scenario 3: urgency is unsupported",
            {
                "product_type": "premium",
                "quantity": 3,
                "region": "JP",
                "urgency": "rush",
            },
        ),
    ]

    try:
        async with Client(SERVER_URL) as client:
            for title, arguments in scenarios:
                await run_error_case(client, title, arguments)
    except Exception as exc:
        print(f"Failed to connect to MCP Server: {exc}")


def main() -> None:
    """Run the error scenario demo."""
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
