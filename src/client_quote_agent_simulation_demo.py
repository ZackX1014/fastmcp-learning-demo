"""QuoteAgent-style simulated workflow demo without a real LLM."""

import asyncio
import json
import re
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"
RESOURCE_URI = "project://summary"
PROMPT_NAME = "analyze_quote_request"

QUOTE_REQUEST_CASES = [
    {
        "name": "Complete request case",
        "requirement_text": (
            "Customer wants 10 standard sensors for JP region with urgent delivery."
        ),
    },
    {
        "name": "Incomplete request case",
        "requirement_text": "Customer wants standard sensors for JP region.",
    },
]


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


def _short_text(value: Any, limit: int = 220) -> str:
    """Keep console output short for beginner-friendly demos."""
    text = _to_json(value) if not isinstance(value, str) else value
    return text if len(text) <= limit else f"{text[:limit]}..."


def simulate_requirement_check(requirement_text: str) -> dict:
    """Simulate a transparent quote requirement completeness check."""
    text = requirement_text.lower()
    extracted: dict[str, Any] = {}
    missing_fields = []

    if "standard sensor" in text or "standard sensors" in text:
        extracted["product_type"] = "standard_sensor"
    elif "premium" in text:
        extracted["product_type"] = "premium"
    elif "standard" in text:
        extracted["product_type"] = "standard"
    else:
        missing_fields.append("product_type")

    quantity_match = re.search(r"\b\d+\b", text)
    if quantity_match:
        extracted["quantity"] = int(quantity_match.group())
    else:
        missing_fields.append("quantity")

    if "jp" in text or "japan" in text:
        extracted["region"] = "JP"
    else:
        missing_fields.append("region")

    if "urgent" in text or "as soon as possible" in text:
        extracted["urgency"] = "urgent"
    elif "normal" in text:
        extracted["urgency"] = "normal"
    else:
        missing_fields.append("urgency")

    return {
        "is_complete": not missing_fields,
        "missing_fields": missing_fields,
        "extracted": extracted,
    }


async def run_quote_request_case(client: Client, case_name: str, requirement_text: str) -> None:
    """Run one QuoteAgent-style simulated request flow."""
    print(f"\n=== {case_name} ===")

    print("\nStep 1: Receive quote request")
    print(requirement_text)

    print("\nStep 2: Load Resource project://summary")
    resource_contents = await client.read_resource(RESOURCE_URI)
    project_summary = _first_resource_value(resource_contents)
    print(_short_text(project_summary))

    print("\nStep 3: Load Prompt analyze_quote_request")
    prompt = await client.get_prompt(
        PROMPT_NAME,
        {
            "requirement_text": requirement_text,
            "customer_region": "JP",
        },
    )
    print(_short_text(_prompt_text(prompt)))

    print("\nStep 4: Simulate requirement completeness check")
    check_result = simulate_requirement_check(requirement_text)
    print(_to_json(check_result))

    print("\nStep 5: Decide whether to call calculate_quote_price")
    if check_result["is_complete"]:
        quote_result = await client.call_tool(
            "calculate_quote_price",
            check_result["extracted"],
        )
        final_result = {
            "case": case_name,
            "called_tool": True,
            "quote_result": quote_result.structured_content,
        }
        print("Tool called: calculate_quote_price")
    else:
        final_result = {
            "case": case_name,
            "called_tool": False,
            "missing_fields": check_result["missing_fields"],
            "message": "Need more information before calculating quote price.",
        }
        print("Tool not called.")

    print("\nStep 6: Final simulated QuoteAgent result")
    print(_to_json(final_result))


async def run_quote_agent_simulation_demo() -> None:
    """Run the QuoteAgent-style simulation for complete and incomplete requests."""
    try:
        async with Client(SERVER_URL) as client:
            for request_case in QUOTE_REQUEST_CASES:
                await run_quote_request_case(
                    client,
                    request_case["name"],
                    request_case["requirement_text"],
                )
    except Exception as exc:
        print(f"Failed to run QuoteAgent simulation demo: {exc}")


def main() -> None:
    """Run the QuoteAgent-style simulation demo."""
    asyncio.run(run_quote_agent_simulation_demo())


if __name__ == "__main__":
    main()
