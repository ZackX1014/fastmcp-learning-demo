"""Resource read demo for the project://summary resource."""

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"
RESOURCE_URI = "project://summary"


def _to_json(value: Any) -> str:
    """Format values for readable console output."""
    return json.dumps(value, ensure_ascii=False, indent=2)


def _parse_resource_text(text: str) -> Any:
    """Parse JSON resource text when possible, otherwise return the raw text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


async def read_project_summary() -> None:
    """Read and print the project summary Resource."""
    try:
        async with Client(SERVER_URL) as client:
            contents = await client.read_resource(RESOURCE_URI)
    except Exception as exc:
        print(f"Failed to read Resource {RESOURCE_URI}: {exc}")
        return

    print(f"Resource: {RESOURCE_URI}")
    for item in contents:
        text = getattr(item, "text", None)
        if text is not None:
            print(_to_json(_parse_resource_text(text)))
        else:
            print(item)


def main() -> None:
    """Run the Resource read demo."""
    asyncio.run(read_project_summary())


if __name__ == "__main__":
    main()
