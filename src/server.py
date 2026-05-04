"""Minimal FastMCP Server for Step 1."""

from fastmcp import FastMCP


mcp = FastMCP("fastmcp-learning-demo")


@mcp.tool
def hello(name: str) -> dict:
    """Return a greeting message for the provided name."""
    if not name.strip():
        return {"success": False, "error": "name is required"}

    return {"success": True, "data": {"message": f"Hello, {name}!"}}


def main() -> None:
    """Run the FastMCP Server with HTTP transport."""
    mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
