# Installation Guide

This guide covers generic MCP client integration patterns and best practices.

## Overview

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external tools and data sources. This server can integrate with any MCP-compatible client.

## MCP Client Types

### Category 1: AI Assistants
- **Claude Code** - CLI tool for AI-assisted development
- **Claude Desktop** - Desktop app with AI chat
- **Continue.dev** - VS Code & JetBrains IDE extension
- **Zed** - Modern code editor with AI

### Category 2: Custom Applications
- **Web Apps** - Using HTTP/SSE transport
- **CLI Tools** - Using stdio transport
- **Automation** - Scripted integrations

## Transport Mechanisms

MCP supports two primary transport methods:

### Stdio (Standard Input/Output)

**Use when:**
- Running locally
- Client can spawn processes
- Direct communication needed

**Configuration:**
```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/server", "run", "mcp-server"],
  "env": {"MCP_SERVER_NAME": "my-server"}
}
```

**Advantages:**
- Simple setup
- Low latency
- No network configuration
- Secure (local only)

### HTTP/SSE (Server-Sent Events)

**Use when:**
- Remote access needed
- Multiple clients connecting
- Web-based integration
- Load balancing required

**Start server:**
```bash
uv run fastmcp run src/mcp_server/server.py:mcp --transport sse --port 8000
```

**Client connection:**
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/rpc",
        json={"method": "tools/list", "params": {}},
    )
```

**Advantages:**
- Remote access
- Language-agnostic
- Scalable
- Web-friendly

## Server Discovery

MCP clients discover servers through:

### 1. Global Configuration

Client-specific config files:
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Continue: `~/.continue/config.json`
- Zed: `~/.config/zed/settings.json`

### 2. Project-Scoped Configuration

`.mcp.json` in project root (Claude Code):
```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "${PROJECT_DIR}", "run", "mcp-server"]
    }
  }
}
```

### 3. CLI Registration

```bash
claude mcp add --transport stdio my-server \
  -- uv --directory /path run mcp-server
```

## Environment Variables

Standard MCP server environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MCP_SERVER_NAME` | string | `mcp-server` | Server identifier |
| `MCP_HOST` | string | `0.0.0.0` | Bind host (HTTP) |
| `MCP_PORT` | integer | `8000` | Listen port (HTTP) |
| `MCP_DEBUG` | boolean | `false` | Debug mode |
| `MCP_LOG_LEVEL` | string | `INFO` | Log level (DEBUG/INFO/WARNING/ERROR) |

**Usage in client config:**
```json
{
  "env": {
    "MCP_SERVER_NAME": "my-custom-server",
    "MCP_DEBUG": "true",
    "MCP_LOG_LEVEL": "DEBUG"
  }
}
```

## Common Configuration Patterns

### Pattern 1: Development vs Production

```json
{
  "mcpServers": {
    "dev-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/dev", "run", "mcp-server"],
      "env": {"MCP_DEBUG": "true", "MCP_LOG_LEVEL": "DEBUG"}
    },
    "prod-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/prod", "run", "mcp-server"],
      "env": {"MCP_LOG_LEVEL": "WARNING"}
    }
  }
}
```

### Pattern 2: Multiple Servers

```json
{
  "mcpServers": {
    "tools-server": {
      "command": "uv",
      "args": ["run", "tools-server"]
    },
    "data-server": {
      "command": "uv",
      "args": ["run", "data-server"]
    }
  }
}
```

### Pattern 3: Custom Environment

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "uv",
      "args": ["run", "mcp-server"],
      "env": {
        "MCP_SERVER_NAME": "custom",
        "DATABASE_URL": "postgresql://localhost/mydb",
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Installation Scripts

### Template Install Script

```bash
#!/bin/bash
set -e

SERVER_NAME="${MCP_SERVER_NAME:-mcp-server}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install dependencies
uv sync

# Register with MCP client
claude mcp add --transport stdio "$SERVER_NAME" \
  --env "MCP_SERVER_NAME=$SERVER_NAME" \
  -- uv --directory "$PROJECT_DIR" run mcp-server

echo "✅ Installed $SERVER_NAME"
```

### Template Uninstall Script

```bash
#!/bin/bash
set -e

SERVER_NAME="${MCP_SERVER_NAME:-mcp-server}"

if claude mcp get "$SERVER_NAME" &> /dev/null; then
    claude mcp remove "$SERVER_NAME"
    echo "✅ Removed $SERVER_NAME"
else
    echo "⚠️  $SERVER_NAME not found"
fi
```

## Troubleshooting

### Server Not Detected

**Check 1**: Verify client supports MCP
```bash
# Claude Code
claude mcp --help

# Continue
grep -i "modelContextProtocol" ~/.continue/config.json
```

**Check 2**: Validate configuration syntax
```bash
# Check JSON is valid
python -m json.tool < config.json
```

**Check 3**: Test server directly
```bash
cd /path/to/server
uv run mcp-server
```

### Connection Errors

**Stdio transport:**
- Verify command path is correct
- Check absolute paths are used
- Ensure execute permissions on scripts

**HTTP/SSE transport:**
- Verify server is running: `curl http://localhost:8000`
- Check firewall settings
- Verify port is not in use: `lsof -i :8000`

### Import Errors

```bash
# Reinstall dependencies
cd /path/to/server
uv sync

# Check Python version
python --version  # Should be 3.11+

# Verify uv is installed
uv --version
```

### Path Issues

**Problem**: `~/` or `./` in paths
**Solution**: Use absolute paths

**macOS/Linux**:
```json
"/Users/username/projects/mcp-template"
```

**Windows**:
```json
"C:\\Users\\username\\projects\\mcp-template"
```

### Permission Issues

```bash
# Make scripts executable
chmod +x install.sh uninstall.sh

# Check file ownership
ls -l /path/to/server
```

## Security Considerations

### Local Integration
- Stdio transport is inherently secure (no network)
- Server runs with user's permissions
- No authentication needed

### Remote Integration
- Use HTTPS/TLS for production
- Implement authentication (API keys, OAuth)
- Validate all inputs
- Use environment variables for secrets
- Restrict CORS appropriately

### Best Practices
1. Never commit secrets to git
2. Use environment variables for sensitive data
3. Validate MCP client identity
4. Log access for audit
5. Rate limit tool calls

## Performance Optimization

### Startup Time
- Use lazy loading for heavy dependencies
- Cache expensive computations
- Minimize import chains

### Response Time
- Use async/await throughout
- Implement connection pooling
- Cache frequent resource reads
- Batch operations when possible

### Resource Usage
- Set memory limits
- Implement timeouts
- Close connections properly
- Monitor resource consumption

## Next Steps

1. **Choose a client**: See [Integration Examples](../examples/integrations/README.md)
2. **Install**: Follow client-specific guide
3. **Customize**: Add your tools, resources, and prompts
4. **Deploy**: Use appropriate transport for your use case
5. **Monitor**: Check logs and performance

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://gofastmcp.com)
- [Integration Examples](../examples/integrations/README.md)
- [Development Guide](../.agents/docs/tooling/development-setup.md)
