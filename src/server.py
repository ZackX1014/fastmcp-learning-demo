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


def main() -> None:
    """Run the FastMCP Server with HTTP transport."""
    mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
