# Zed Editor Integration

Configure this MCP server with Zed editor's assistant.

## Installation

### 1. Install Zed

Download from [zed.dev](https://zed.dev/)

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/mcp-template.git
cd mcp-template
uv sync
```

### 3. Configure Zed Settings

Open Zed settings:
- **macOS**: `Cmd + ,` or `~/.config/zed/settings.json`
- **Linux**: `Ctrl + ,` or `~/.config/zed/settings.json`
- **Windows**: `Ctrl + ,` or `%APPDATA%\Zed\settings.json`

### 4. Add Context Server

Add the following to your `settings.json`:

```json
{
  "context_servers": {
    "mcp-server": {
      "command": {
        "path": "uv",
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
}
```

**Important**: Replace `/absolute/path/to/mcp-template` with your actual project path.

### 5. Restart Zed

Close and reopen Zed for changes to take effect.

## Configuration Options

### Custom Environment Variables

```json
{
  "context_servers": {
    "mcp-server": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/project", "run", "mcp-server"],
        "env": {
          "MCP_SERVER_NAME": "my-server",
          "MCP_DEBUG": "true",
          "MCP_LOG_LEVEL": "DEBUG"
        }
      }
    }
  }
}
```

### Multiple Servers

```json
{
  "context_servers": {
    "mcp-server-dev": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/mcp-template", "run", "mcp-server"],
        "env": {"MCP_SERVER_NAME": "dev-server"}
      }
    },
    "mcp-server-prod": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/mcp-template", "run", "mcp-server"],
        "env": {"MCP_SERVER_NAME": "prod-server"}
      }
    }
  }
}
```

## Using in Zed

Once configured:

1. Open Zed Assistant panel (`Cmd/Ctrl + ?`)
2. Start a conversation
3. Your MCP tools will be available for the assistant to use
4. Resources and prompts are accessible in the context

## Troubleshooting

### Server not loading

1. Check Zed settings syntax is valid JSON
2. Verify absolute paths are used
3. Ensure uv and dependencies are installed
4. Check Zed logs

### View Logs

Open Zed's developer console:
- **macOS**: `Cmd + Alt + I`
- **Linux/Windows**: `Ctrl + Alt + I`

### Import errors

Ensure dependencies are installed:
```bash
cd /path/to/mcp-template
uv sync
```

### Path issues

**macOS/Linux**: Use full path `/Users/username/projects/mcp-template`
**Windows**: Use full path `C:\\Users\\username\\projects\\mcp-template`

## Features

Zed integration provides:
- Context-aware AI assistance
- Tool calling in conversations
- Access to project resources
- Custom prompts integration
- Real-time code understanding

## Performance

Zed's MCP integration is optimized for:
- Fast tool discovery
- Low latency responses
- Efficient resource loading
- Minimal memory overhead

## Uninstallation

Remove the server entry from Zed's `settings.json` and restart the editor.

## See Also

- [Zed Documentation](https://zed.dev/docs)
- [Zed MCP Support](https://zed.dev/docs/assistant/context-servers)
- [Main README](../../../README.md)
