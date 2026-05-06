"""Prompt demo for the analyze_quote_request prompt."""

import asyncio

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"
PROMPT_NAME = "analyze_quote_request"


async def get_quote_analysis_prompt() -> None:
    """Get and print the quote analysis Prompt."""
    try:
        async with Client(SERVER_URL) as client:
            prompt = await client.get_prompt(
                PROMPT_NAME,
                {
                    "requirement_text": (
                        "We need 3 premium devices for our Tokyo office as soon as possible."
                    ),
                    "customer_region": "JP",
                },
            )
    except Exception as exc:
        print(f"Failed to get Prompt {PROMPT_NAME}: {exc}")
        return

    print(f"Prompt: {PROMPT_NAME}")
    if prompt.description:
        print(f"Description: {prompt.description}")

    for index, message in enumerate(prompt.messages, start=1):
        print(f"\nMessage {index} ({message.role}):")
        content = message.content
        text = getattr(content, "text", None)
        print(text if text is not None else content)


def main() -> None:
    """Run the Prompt demo."""
    asyncio.run(get_quote_analysis_prompt())


if __name__ == "__main__":
    main()
