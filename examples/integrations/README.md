# MCP Client Integrations

This directory contains integration examples for various MCP clients. Choose the integration that matches your use case.

## Available Integrations

### Claude Code
**Best for**: CLI users, developers
**Installation time**: 30 seconds - 2 minutes

Integrate with Claude Code CLI for powerful AI-assisted development.

[→ See Claude Code Integration](claude-code/README.md)

### Claude Desktop
**Best for**: Desktop app users
**Installation time**: 5 minutes

Configure the Claude Desktop app to use your MCP server.

[→ See Claude Desktop Integration](claude-desktop/README.md)

### Continue.dev
**Best for**: VS Code and JetBrains users
**Installation time**: 5 minutes

Add MCP tools to Continue's AI coding assistant in your IDE.

[→ See Continue Integration](continue/README.md)

### Zed Editor
**Best for**: Zed editor users
**Installation time**: 5 minutes

Configure Zed's AI assistant to use your MCP server.

[→ See Zed Integration](zed/README.md)

### Custom Client
**Best for**: Programmatic access, custom tools
**Installation time**: Varies

Build your own MCP client for custom integration scenarios.

[→ See Custom Client Guide](custom/README.md)

## Quick Comparison

| Client | Type | Ease of Use | Best For |
|--------|------|-------------|----------|
| **Claude Code** | CLI | ⭐⭐⭐⭐⭐ | Development, command line |
| **Claude Desktop** | Desktop App | ⭐⭐⭐⭐ | General usage, conversations |
| **Continue.dev** | IDE Extension | ⭐⭐⭐⭐ | VS Code, JetBrains IDEs |
| **Zed** | Editor | ⭐⭐⭐⭐ | Modern text editing |
| **Custom** | Programmatic | ⭐⭐⭐ | Custom integrations, APIs |

## Installation Methods

### Direct from GitHub (No Clone)

For Claude Code, you can install directly:

```bash
claude mcp add --transport stdio mcp-server \
  -- uv run --with "git+https://github.com/YOUR-USERNAME/mcp-template.git" mcp-server
```

### Local Development

All integrations support local development:

1. Clone the repository
2. Install dependencies with `uv sync`
3. Follow client-specific setup in respective directories

### Project-Scoped (Teams)

Commit `.mcp.json` (Claude Code) or configuration files to version control for team-wide setup.

## Transport Types

### Stdio (Standard Input/Output)
- **Used by**: Claude Code, Claude Desktop, Continue, Zed, Custom
- **Best for**: Local integrations
- **Setup**: Direct process communication

### HTTP/SSE (Server-Sent Events)
- **Used by**: Custom clients, web apps
- **Best for**: Remote access, web integration
- **Setup**: Run server with `--transport sse`

## Configuration

All integrations use environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_NAME` | `mcp-server` | Server identifier |
| `MCP_HOST` | `0.0.0.0` | Host (HTTP mode) |
| `MCP_PORT` | `8000` | Port (HTTP mode) |
| `MCP_DEBUG` | `false` | Enable debug mode |
| `MCP_LOG_LEVEL` | `INFO` | Logging level |

## Troubleshooting

### Common Issues

**Server not appearing:**
- Verify client is installed
- Check configuration file syntax
- Ensure absolute paths are used
- Restart client application

**Import errors:**
```bash
cd /path/to/mcp-template
uv sync
```

**Path problems:**
- Use absolute paths (not `~/` or `./`)
- macOS/Linux: `/Users/username/projects/mcp-template`
- Windows: `C:\\Users\\username\\projects\\mcp-template`

### Getting Help

1. Check client-specific README for detailed troubleshooting
2. Review client logs for error messages
3. Verify MCP server works standalone: `uv run mcp-server`
4. Check [GitHub Issues](https://github.com/YOUR-USERNAME/mcp-template/issues)

## Next Steps

1. Choose your MCP client from the list above
2. Follow the integration guide for that client
3. Customize your MCP server in `src/mcp_server/`
4. Read the [Development Guide](../../.agents/docs/tooling/development-setup.md)

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Main README](../../README.md)
- [Project Structure](../../.agents/docs/conventions/project-structure.md)
