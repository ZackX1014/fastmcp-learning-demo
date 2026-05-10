"""Simulated Agent workflow demo using Resource, Prompt, and Tool."""

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"
RESOURCE_URI = "project://summary"
PROMPT_NAME = "analyze_quote_request"
REQUIREMENT_TEXT = "Customer wants 10 standard sensors for JP region with urgent delivery."
CUSTOMER_REGION = "JP"
QUOTE_ARGUMENTS = {
    "product_type": "standard_sensor",
    "quantity": 10,
    "region": "JP",
    "urgency": "urgent",
}


def _to_json(value: Any) -> str:
    """Format values for readable console output."""
    return json.dumps(value, ensure_ascii=False, indent=2)


def _parse_json_text(text: str) -> Any:
    """Parse JSON text when possible, otherwise return the raw text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _first_resource_value(contents: list[Any]) -> Any:
    """Extract the first Resource value for simple demo output."""
    if not contents:
        return None

    text = getattr(contents[0], "text", None)
    if text is None:
        return contents[0]

    return _parse_json_text(text)


def _prompt_text(prompt: Any) -> str:
    """Extract readable text from the first Prompt message."""
    if not prompt.messages:
        return ""

    content = prompt.messages[0].content
    text = getattr(content, "text", None)
    return text if text is not None else str(content)


async def run_agent_workflow_demo() -> None:
    """Run a small simulated Agent workflow without connecting to a real LLM."""
    try:
        async with Client(SERVER_URL) as client:
            print("Step 1: Loaded Resource")
            resource_contents = await client.read_resource(RESOURCE_URI)
            project_summary = _first_resource_value(resource_contents)
            print(_to_json(project_summary))

            print("\nStep 2: Loaded Prompt")
            prompt = await client.get_prompt(
                PROMPT_NAME,
                {
                    "requirement_text": REQUIREMENT_TEXT,
                    "customer_region": CUSTOMER_REGION,
                },
            )
            prompt_text = _prompt_text(prompt)
            print(prompt_text)

            print("\nStep 3: Called Tool")
            quote_result = await client.call_tool(
                "calculate_quote_price",
                QUOTE_ARGUMENTS,
            )
            print(_to_json(quote_result.structured_content))

            print("\nFinal Simulated Agent Workflow Result")
            quote_data = quote_result.structured_content.get("data", {})
            print(
                _to_json(
                    {
                        "resource": RESOURCE_URI,
                        "prompt": PROMPT_NAME,
                        "tool": "calculate_quote_price",
                        "requirement_text": REQUIREMENT_TEXT,
                        "total_price": quote_data.get("total_price"),
                        "currency": quote_data.get("currency"),
                        "note": "No real LLM was used. The Client only orchestrated MCP calls.",
                    }
                )
            )
    except Exception as exc:
        print(f"Failed to run simulated Agent workflow: {exc}")


def main() -> None:
    """Run the simulated Agent workflow demo."""
    asyncio.run(run_agent_workflow_demo())


if __name__ == "__main__":
    main()
