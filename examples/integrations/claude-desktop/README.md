# Claude Desktop Integration

Configure this MCP server with Claude Desktop app.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/mcp-template.git
cd mcp-template
uv sync
```

### 2. Locate Claude Desktop Config

The config file location depends on your OS:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 3. Add Server Configuration

Edit the config file and add the server:

```json
{
  "mcpServers": {
    "mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-template",
        "run",
        "mcp-server"
      ],
      "env": {
        "MCP_SERVER_NAME": "mcp-server"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/mcp-template` with your actual project path.

### 4. Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

### 5. Verify Installation

In Claude Desktop, you should see your MCP tools available in the conversation.

## Configuration Options

### Environment Variables

```json
{
  "mcpServers": {
    "mcp-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/project", "run", "mcp-server"],
      "env": {
        "MCP_SERVER_NAME": "my-custom-server",
        "MCP_DEBUG": "true",
        "MCP_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Multiple Servers

You can run multiple instances with different configurations:

```json
{
  "mcpServers": {
    "mcp-server-dev": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-template", "run", "mcp-server"],
      "env": {
        "MCP_SERVER_NAME": "mcp-server-dev",
        "MCP_DEBUG": "true"
      }
    },
    "mcp-server-prod": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-template", "run", "mcp-server"],
      "env": {
        "MCP_SERVER_NAME": "mcp-server-prod"
      }
    }
  }
}
```

## Troubleshooting

### Server not appearing

1. Check config file location is correct for your OS
2. Verify JSON syntax is valid
3. Ensure absolute paths are used
4. Restart Claude Desktop completely

### Import errors

Ensure dependencies are installed:
```bash
cd /path/to/mcp-template
uv sync
```

### Path issues

Use absolute paths, not relative paths like `~/` or `./`

**macOS/Linux**: Use full path like `/Users/username/projects/mcp-template`

**Windows**: Use full path like `C:\Users\username\projects\mcp-template`

## Logs

Check Claude Desktop logs for errors:

- **macOS**: `~/Library/Logs/Claude/`
- **Windows**: `%APPDATA%\Claude\logs\`
- **Linux**: `~/.config/Claude/logs/`

## Uninstallation

Remove the server entry from `claude_desktop_config.json` and restart Claude Desktop.

## See Also

- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs/claude-desktop)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Main README](../../../README.md)
