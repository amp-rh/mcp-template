# Continue.dev Integration

Configure this MCP server with Continue.dev VS Code/JetBrains extension.

## Installation

### 1. Install Continue Extension

- **VS Code**: Install from [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=Continue.continue)
- **JetBrains**: Install from [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/22707-continue)

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/mcp-template.git
cd mcp-template
uv sync
```

### 3. Locate Continue Config

The config file location:

- **VS Code**: `~/.continue/config.json`
- **JetBrains**: `~/.continue/config.json`

### 4. Add MCP Server Configuration

Edit `config.json` and add to the `experimental` section:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
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
    ]
  }
}
```

**Important**: Replace `/absolute/path/to/mcp-template` with your actual project path.

### 5. Reload Extension

Reload the Continue extension or restart your IDE.

## Configuration Options

### With Custom Environment Variables

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uv",
          "args": ["--directory", "/path/to/project", "run", "mcp-server"],
          "env": {
            "MCP_SERVER_NAME": "my-server",
            "MCP_DEBUG": "true",
            "MCP_LOG_LEVEL": "DEBUG"
          }
        }
      }
    ]
  }
}
```

### Multiple Servers

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uv",
          "args": ["--directory", "/path/to/mcp-template", "run", "mcp-server"],
          "env": {"MCP_SERVER_NAME": "server-1"}
        }
      },
      {
        "transport": {
          "type": "stdio",
          "command": "uv",
          "args": ["--directory", "/path/to/other-server", "run", "mcp-server"],
          "env": {"MCP_SERVER_NAME": "server-2"}
        }
      }
    ]
  }
}
```

## Using MCP Tools in Continue

Once configured, MCP tools will be available in Continue's context:

1. Open Continue sidebar in your IDE
2. Start a conversation
3. MCP tools will be automatically available for the AI to use
4. The AI can call your tools to perform actions

## Troubleshooting

### Server not loading

1. Check Continue extension is installed and enabled
2. Verify config.json syntax is valid JSON
3. Ensure absolute paths are used (not `~/` or `./`)
4. Check Continue logs for errors

### View Logs

**VS Code**:
- Open Command Palette (`Cmd/Ctrl + Shift + P`)
- Run "Continue: Show Logs"

**JetBrains**:
- Help → Show Log in Finder/Explorer

### Import errors

Ensure dependencies are installed:
```bash
cd /path/to/mcp-template
uv sync
```

### Path issues

**macOS/Linux**: Use `/Users/username/projects/mcp-template`
**Windows**: Use `C:\\Users\\username\\projects\\mcp-template` (double backslashes)

## Features

Continue integration provides:
- Tool calling within IDE conversations
- Access to project resources
- Custom prompts for code generation
- Seamless context from your MCP server

## Uninstallation

Remove the server entry from `~/.continue/config.json` and reload the extension.

## See Also

- [Continue Documentation](https://docs.continue.dev/)
- [Continue MCP Support](https://docs.continue.dev/features/model-context-protocol)
- [Main README](../../../README.md)
