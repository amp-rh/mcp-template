"""MCP Server Template.

A FastMCP server template with organized tools, resources, and prompts.
"""

__version__ = "0.1.0"

from mcp_server.server import create_server, mcp

__all__ = ["__version__", "create_server", "mcp"]
