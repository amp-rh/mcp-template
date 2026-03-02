# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server template built with FastMCP. It provides organized modules for tools, resources, and prompts with HTTP/SSE transport support. The project follows a modular architecture with comprehensive AGENTS.md documentation system.

## Development Commands

### Package Management (uv)
```bash
uv sync                    # Install production dependencies
uv sync --extra dev        # Install with dev dependencies
```

### Running the Server
```bash
# Production mode (HTTP/SSE on port 8000)
uv run fastmcp run src/mcp_server/server.py:mcp --transport sse --port 8000

# Development mode with auto-reload
uv run fastmcp dev src/mcp_server/server.py:mcp --transport sse --port 8000

# CLI mode (stdio transport)
uv run fastmcp run src/mcp_server/server.py:mcp --transport stdio

# Using make targets
make run        # Production mode
make run-dev    # Development mode
```

### Testing
```bash
uv run pytest                              # Run all tests
uv run pytest --cov=src --cov-report=term-missing  # With coverage
uv run pytest tests/test_tools.py -v      # Run specific test file
uv run pytest -k test_name                # Run specific test

make test       # Run all tests
make test-cov   # Run with coverage
```

### Linting and Formatting
```bash
uv run ruff check .           # Run linting
uv run ruff format .          # Format code
uv run ruff check --fix .     # Auto-fix issues
uv run mypy src               # Type checking

make lint       # Lint
make format     # Format and fix
make typecheck  # Type checking
make check      # Lint + test
make check-all  # Format + lint + typecheck + test
```

### Container Operations
```bash
make build          # Build podman/docker image
make run-container  # Run container
```

## Architecture

### Server Factory Pattern

The server is created via a factory function in `server.py` that composes all MCP components:

```python
def create_server(config: ServerConfig | None = None) -> FastMCP:
    config = config or ServerConfig.from_env()
    server = FastMCP(config.name)
    register_tools(server)      # Register all tools
    register_resources(server)  # Register all resources
    register_prompts(server)    # Register all prompts
    return server
```

### Module Registration Pattern

Each component type (tools, resources, prompts) has its own module with a `register_*()` function:

- **Tools** (`src/mcp_server/tools/`): Functions AI can call to perform actions
- **Resources** (`src/mcp_server/resources/`): Data sources AI can read (URI-based)
- **Prompts** (`src/mcp_server/prompts/`): Reusable prompt templates

All components use decorators (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`) and are lazy-loaded when imported.

### Configuration

Configuration uses immutable dataclasses with environment variable support:

```python
@dataclass(frozen=True)
class ServerConfig:
    name: str = "mcp-server"
    host: str = "0.0.0.0"
    port: int = 8000

    @classmethod
    def from_env(cls) -> "ServerConfig":
        # Reads from MCP_SERVER_NAME, MCP_HOST, MCP_PORT
```

## Adding New Components

### Adding a Tool

1. Create file in `src/mcp_server/tools/` (e.g., `weather_tools.py`)
2. Define tools using `@mcp.tool` decorator
3. Import in `tools/__init__.py` register function
4. Add tests in `tests/test_tools.py`

Example:
```python
@mcp.tool
def fetch_weather(city: str, units: str = "metric") -> dict:
    """Fetch weather data for a city."""
    return {"city": city, "temp": 72, "condition": "sunny"}
```

### Adding a Resource

1. Create file in `src/mcp_server/resources/`
2. Define resources with URI patterns using `@mcp.resource`
3. Import in `resources/__init__.py` register function
4. Add tests in `tests/test_resources.py`

Resources must return strings (use `json.dumps()` for structured data).

### Adding a Prompt

1. Create file in `src/mcp_server/prompts/`
2. Define prompts using `@mcp.prompt` decorator
3. Import in `prompts/__init__.py` register function
4. Add tests in `tests/test_prompts.py`

## AGENTS.md System

This project uses a hierarchical AGENTS.md documentation system. Before modifying any directory:

1. Read the `AGENTS.md` file in that directory
2. Follow references to detailed docs in `.agents/docs/`
3. Update documentation when discovering new patterns

Key documentation locations:
- `/AGENTS.md` - Root index, project overview, core rules
- `.agents/docs/tooling/` - uv, pytest, ruff, fastmcp
- `.agents/docs/patterns/` - Error handling, typing, MCP patterns
- `.agents/docs/conventions/` - Coding style, naming, imports, structure
- `.agents/docs/workflows/` - Testing, PR process, releases

## Code Style Requirements

- **No comments**: Code must self-document through clear naming and structure
- **Dataclasses**: Use `@dataclass` for all data structures, `frozen=True` for immutable
- **Type hints**: All functions must have complete type annotations
- **Small functions**: Prefer functions under 10 lines
- **Single responsibility**: Each class/function does one thing
- **TDD**: Write tests before implementation

## Testing Requirements

- Run `pytest` before committing any changes
- Maintain >90% coverage for domain/application logic
- Use `pytest-asyncio` for async tests (`@pytest.mark.asyncio`)
- Test files mirror source structure (`test_tools.py` for `tools/`)

## Critical Rules

1. MUST read relevant `AGENTS.md` before modifying any directory
2. MUST run `uv sync` after modifying `pyproject.toml`
3. MUST run `pytest` before committing changes
4. MUST use registration pattern for all MCP components
5. MUST follow MCP patterns in `.agents/docs/patterns/mcp-patterns.md`
6. Resources MUST return strings (use `json.dumps()` for objects)
7. All dataclasses SHOULD be frozen for immutability
8. Configuration MUST use environment variables via `ServerConfig.from_env()`
