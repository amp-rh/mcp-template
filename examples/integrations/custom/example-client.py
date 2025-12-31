#!/usr/bin/env python3
"""
Example custom MCP client that connects to the server.

This demonstrates how to build a custom client that communicates
with an MCP server using the stdio transport.
"""

import asyncio
import json
import subprocess
from typing import Any


class MCPClient:
    """Simple MCP client using stdio transport."""

    def __init__(self, command: list[str]):
        self.command = command
        self.process: subprocess.Popen | None = None

    async def start(self) -> None:
        """Start the MCP server process."""
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print("✅ MCP server started")

    async def send_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a JSON-RPC request to the server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("Server not started")

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }

        request_json = json.dumps(request)
        print(f"📤 Sending: {method}")
        self.process.stdin.write(request_json + "\n")
        self.process.stdin.flush()

        if not self.process.stdout:
            raise RuntimeError("No stdout available")

        response_line = self.process.stdout.readline()
        response = json.loads(response_line)
        print(f"📥 Received response for: {method}")
        return response

    async def list_tools(self) -> list[dict[str, Any]]:
        """List available tools."""
        response = await self.send_request("tools/list")
        return response.get("result", {}).get("tools", [])

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call a specific tool."""
        response = await self.send_request(
            "tools/call",
            {"name": name, "arguments": arguments},
        )
        return response.get("result")

    async def list_resources(self) -> list[dict[str, Any]]:
        """List available resources."""
        response = await self.send_request("resources/list")
        return response.get("result", {}).get("resources", [])

    async def read_resource(self, uri: str) -> Any:
        """Read a specific resource."""
        response = await self.send_request("resources/read", {"uri": uri})
        return response.get("result")

    async def stop(self) -> None:
        """Stop the MCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🛑 MCP server stopped")


async def main() -> None:
    """Example usage of the custom MCP client."""
    # Configure the MCP server command
    server_command = [
        "uv",
        "--directory",
        "/absolute/path/to/mcp-template",  # Update this path
        "run",
        "mcp-server",
    ]

    client = MCPClient(server_command)

    try:
        # Start the server
        await client.start()

        # Initialize the connection
        await client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "custom-client",
                "version": "1.0.0",
            },
        })

        # List available tools
        print("\n📋 Available Tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool.get('name')}: {tool.get('description')}")

        # Call a tool (example: greet tool)
        print("\n🔧 Calling 'greet' tool:")
        result = await client.call_tool("greet", {"name": "World"})
        print(f"  Result: {result}")

        # List available resources
        print("\n📚 Available Resources:")
        resources = await client.list_resources()
        for resource in resources:
            print(f"  - {resource.get('uri')}: {resource.get('name')}")

        # Read a resource (example)
        if resources:
            uri = resources[0].get("uri")
            print(f"\n📖 Reading resource '{uri}':")
            content = await client.read_resource(uri)
            print(f"  Content: {content}")

    finally:
        # Clean up
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
