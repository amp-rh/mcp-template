# Claude Code Integration

Install this MCP server with Claude Code using one of the methods below.

## Quick Installation

### Option 1: Direct from GitHub (No Clone Required)

Install directly from GitHub with one command:

```bash
claude mcp add --transport stdio mcp-server \
  -- uv run --with "git+https://github.com/YOUR-USERNAME/mcp-template.git" mcp-server
```

**Advantages:**
- No need to clone the repository
- Always uses latest version
- One command installation
- Perfect for end users

**Verify installation:**
```bash
claude mcp list
```

### Option 2: Automated Script (Local Development)

For local development with the cloned repository:

```bash
# From the project root
./examples/integrations/claude-code/install.sh
```

Or using make:
```bash
make install-claude
```

The script will:
- Check prerequisites (Claude Code CLI, uv)
- Install dependencies
- Configure Claude Code automatically
- Verify installation

### Option 3: Project-Scoped Configuration

This project includes a `.mcp.json` file. When you open Claude Code in this directory:

1. Claude Code detects the `.mcp.json` configuration
2. Prompts you to approve the MCP server
3. Automatically configures it for this project

**Advantage**: Team members can use the same configuration (commit `.mcp.json` to git)

### Option 4: Manual Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/mcp-template.git
cd mcp-template

# Install dependencies
uv sync

# Add to Claude Code
claude mcp add --transport stdio mcp-server \
  --env MCP_SERVER_NAME=mcp-server \
  -- uv --directory "$(pwd)" run mcp-server

# Verify
claude mcp list
```

## Installation Methods Comparison

| Method | Best For | Time | Pros | Cons |
|--------|----------|------|------|------|
| Direct from GitHub | End users | 30 sec | No clone needed, one command | Can't customize easily |
| Automated script | Local development | 2 min | Easy setup, customizable | Requires clone |
| Project-scoped | Teams | 1 min | Shared config, version control | Requires clone |
| Manual | Advanced users | 5 min | Full control | More steps |

## Using the Server

After installation, in Claude Code:

1. Type `/mcp` to see available tools, resources, and prompts
2. Use tools in your conversation naturally
3. Access resources with URI patterns
4. Invoke prompts for specialized workflows

## Customization

Edit the server components:

```bash
# Tools (functions AI can call)
src/mcp_server/tools/

# Resources (data sources AI can read)
src/mcp_server/resources/

# Prompts (reusable prompt templates)
src/mcp_server/prompts/
```

After making changes, reload the server:
```bash
claude mcp reload mcp-server
```

## Configuration

The server uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_NAME` | `mcp-server` | Server name |
| `MCP_HOST` | `0.0.0.0` | Host (HTTP mode only) |
| `MCP_PORT` | `8000` | Port (HTTP mode only) |

Edit these in `.mcp.json` or pass via `--env` flag.

## Uninstallation

### Using Script

```bash
./examples/integrations/claude-code/uninstall.sh
```

Or using make:
```bash
make uninstall-claude
```

### Manual

```bash
claude mcp remove mcp-server
```

## Troubleshooting

### Server not appearing in `/mcp`

```bash
# Check if server is registered
claude mcp list

# Check server logs
claude mcp logs mcp-server

# Reload the server
claude mcp reload mcp-server
```

### Import errors

Ensure dependencies are installed:
```bash
cd /path/to/mcp-template
uv sync
```

### Permission denied on scripts

Make scripts executable:
```bash
chmod +x examples/integrations/claude-code/*.sh
```

## Next Steps

- Read the [main README](../../../README.md) for project overview
- See [Development Setup](../../../.agents/docs/tooling/development-setup.md) for development guide
- Check [AGENTS.md](../../../AGENTS.md) for AI agent guidance

## Support

- GitHub Issues: https://github.com/YOUR-USERNAME/mcp-template/issues
- MCP Documentation: https://modelcontextprotocol.io
- Claude Code: https://claude.com/code
