# Custom MCP Client Integration

Build custom clients to integrate with your MCP server programmatically.

## Overview

This example demonstrates how to create a custom MCP client that communicates with the server using:
- Stdio transport (standard input/output)
- JSON-RPC protocol
- Async/await patterns

## Example Client

See `example-client.py` for a complete working example.

## Usage

### 1. Update the Script

Edit `example-client.py` and update the server path:

```python
server_command = [
    "uv",
    "--directory",
    "/absolute/path/to/mcp-template",  # Update this!
    "run",
    "mcp-server",
]
```

### 2. Run the Example

```bash
python examples/integrations/custom/example-client.py
```

The script will:
1. Start the MCP server as a subprocess
2. Initialize the connection
3. List available tools
4. Call a tool example
5. List and read resources
6. Clean up and stop the server

## Building Your Own Client

### Basic Structure

```python
import asyncio
import json
import subprocess


class MCPClient:
    def __init__(self, command: list[str]):
        self.command = command
        self.process = None

    async def start(self):
        """Start MCP server as subprocess."""
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

    async def send_request(self, method: str, params: dict = None):
        """Send JSON-RPC request."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        response = json.loads(self.process.stdout.readline())
        return response
```

### Initialize Connection

```python
await client.send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
        "name": "my-client",
        "version": "1.0.0",
    },
})
```

### Call Tools

```python
# List tools
tools = await client.send_request("tools/list")

# Call a specific tool
result = await client.send_request("tools/call", {
    "name": "greet",
    "arguments": {"name": "World"},
})
```

### Access Resources

```python
# List resources
resources = await client.send_request("resources/list")

# Read a resource
content = await client.send_request("resources/read", {
    "uri": "config://settings",
})
```

### Use Prompts

```python
# List prompts
prompts = await client.send_request("prompts/list")

# Get a prompt
prompt = await client.send_request("prompts/get", {
    "name": "code_review",
    "arguments": {
        "code": "def hello(): pass",
        "language": "python",
    },
})
```

## Transport Options

### Stdio Transport (Default)

Best for:
- CLI applications
- Local integrations
- Simple setups

```python
server_command = ["uv", "--directory", "/path", "run", "mcp-server"]
```

### HTTP/SSE Transport

Best for:
- Web applications
- Remote servers
- Distributed systems

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/rpc",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        },
    )
```

## MCP Protocol

### JSON-RPC Format

All MCP messages use JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method/name",
  "params": {}
}
```

### Core Methods

| Method | Description |
|--------|-------------|
| `initialize` | Initialize connection |
| `tools/list` | List available tools |
| `tools/call` | Call a tool |
| `resources/list` | List resources |
| `resources/read` | Read a resource |
| `prompts/list` | List prompts |
| `prompts/get` | Get a prompt |

## Use Cases

### Custom CLI Tool

```python
#!/usr/bin/env python3
import asyncio
from mcp_client import MCPClient

async def main():
    client = MCPClient(["uv", "run", "mcp-server"])
    await client.start()

    # Your custom logic here
    result = await client.call_tool("my_tool", {"param": "value"})
    print(result)

    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Web Backend Integration

```python
from fastapi import FastAPI
from mcp_client import MCPClient

app = FastAPI()
mcp = MCPClient(["uv", "run", "mcp-server"])

@app.on_event("startup")
async def startup():
    await mcp.start()

@app.post("/api/process")
async def process(data: dict):
    result = await mcp.call_tool("process_data", data)
    return {"result": result}
```

### Test Automation

```python
import pytest
from mcp_client import MCPClient

@pytest.fixture
async def mcp_client():
    client = MCPClient(["uv", "run", "mcp-server"])
    await client.start()
    yield client
    await client.stop()

async def test_tool(mcp_client):
    result = await mcp_client.call_tool("test_tool", {})
    assert result["status"] == "success"
```

## Error Handling

```python
try:
    result = await client.call_tool("risky_tool", {})
except Exception as e:
    print(f"Tool failed: {e}")
    # Handle error
```

## Best Practices

1. **Always clean up**: Stop the server process when done
2. **Handle errors**: Wrap calls in try/except blocks
3. **Validate responses**: Check response format and errors
4. **Use async/await**: MCP is designed for async operation
5. **Set timeouts**: Prevent hanging on slow operations
6. **Log communication**: Debug protocol issues

## Dependencies

For custom clients, you'll need:

```bash
# For basic stdio client
pip install asyncio  # (built-in to Python 3.7+)

# For HTTP client
pip install httpx

# For SSE client
pip install httpx-sse
```

## See Also

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Main README](../../../README.md)
