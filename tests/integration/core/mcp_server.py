from blaxel.core.mcp.server import FastMCP

mcp = FastMCP("My App")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


def main():
    """Main function for standalone execution."""
    print("Testing MCP server creation...")

    # Test server creation
    assert mcp is not None
    assert mcp.name == "My App"
    print("✓ MCP server creation test passed")

    # Test tool registration
    result = add(1, 2)
    assert result == 3
    print("✓ MCP tool registration test passed")

    # Test resource registration
    result = get_greeting("World")
    assert result == "Hello, World!"
    print("✓ MCP resource registration test passed")

    print("✅ All MCP server tests passed!")

    print("🚀 Starting MCP WebSocket server on port 8080...")
    # Run the server
    mcp.run(transport="ws")


if __name__ == "__main__":
    main()
