from mcp.server.mcpserver import MCPServer
mcp = MCPServer("Hello MCP")
@mcp.tool()
def get_greeting(name: str) -> str:
	"""Return a greeting for a student."""
	return f"Hello, {name}! Your first MCP tool works."
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
	"""Add two numbers."""
	return a + b
if __name__ == "__main__":
	mcp.run()