"""FastMCP learning demo server."""

from fastmcp import FastMCP


mcp = FastMCP("fastmcp-learning-demo")


@mcp.tool
def hello(name: str) -> dict:
    """Return a greeting message for the provided name."""
    if not name.strip():
        return {"success": False, "error": "name is required"}

    return {"success": True, "data": {"message": f"Hello, {name}!"}}


@mcp.tool
def calculate_quote_price(
    product_type: str,
    quantity: int,
    region: str = "JP",
    urgency: str = "normal",
) -> dict:
    """Calculate a simple quote price using local demo pricing rules."""
    product_type = product_type.strip().lower()
    region = region.strip().upper()
    urgency = urgency.strip().lower()

    if not product_type:
        return {"success": False, "error": "product_type is required."}
    if quantity <= 0:
        return {"success": False, "error": "quantity must be greater than 0."}
    if not region:
        return {"success": False, "error": "region is required."}
    if urgency not in {"normal", "urgent"}:
        return {
            "success": False,
            "error": "urgency must be either 'normal' or 'urgent'.",
        }

    unit_prices = {
        "standard": 100,
        "premium": 200,
    }
    unit_price = unit_prices.get(product_type, 150)
    subtotal = unit_price * quantity
    urgency_fee = int(subtotal * 0.2) if urgency == "urgent" else 0
    total_price = subtotal + urgency_fee

    return {
        "success": True,
        "data": {
            "product_type": product_type,
            "quantity": quantity,
            "region": region,
            "urgency": urgency,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "urgency_fee": urgency_fee,
            "total_price": total_price,
            "currency": "JPY",
        },
    }


@mcp.resource(
    "project://summary",
    name="project_summary",
    description="Read a short summary of the FastMCP learning demo project.",
    mime_type="application/json",
)
def get_project_summary() -> dict:
    """Return a read-only summary of this learning project."""
    return {
        "project_name": "fastmcp-learning-demo",
        "project_type": "FastMCP / MCP learning demo",
        "goal": "learn FastMCP Server, Tool, Client, HTTP Transport, Resource, Prompt",
        "completed_steps": [
            "Step 1: FastMCP Server and hello tool",
            "Step 2: MCP Client calls hello tool",
            "Step 3: quote price calculator tool",
            "Step 4: tool validation and error handling demo",
        ],
        "current_focus": "learning MCP Resource",
        "note": "this project does not connect to the real QuoteAgent system",
    }


@mcp.prompt(
    name="analyze_quote_request",
    description="Create a reusable instruction template for quote request analysis.",
)
def analyze_quote_request(
    requirement_text: str,
    customer_region: str = "JP",
) -> str:
    """Render a quote request analysis prompt for learning MCP Prompt."""
    return f"""You are a quote request analysis assistant.

This is a FastMCP / MCP learning demo.
It does not connect to the real QuoteAgent system.

Read the user's quote request and identify:

1. Product type
2. Quantity
3. Customer region
4. Urgency

If information is missing, list the questions that must be confirmed.
Do not invent missing information.
Do not calculate the price directly.
Use a clear structure in your response.

Customer region:
{customer_region}

Quote request text:
{requirement_text}
"""


def main() -> None:
    """Run the FastMCP Server with HTTP transport."""
    mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
