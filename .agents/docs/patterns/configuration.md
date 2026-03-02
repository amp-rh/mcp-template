# Configuration Patterns

See @AGENTS.md for project-wide rules.

## Overview

This guide covers configuration management patterns for MCP servers, including environment variables, validation, and multiple configuration sources.

## Configuration Dataclass

Use frozen dataclasses for configuration:

```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class ServerConfig:
    name: str = "mcp-server"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
```

## Multiple Configuration Sources

### From Environment Variables

```python
@classmethod
def from_env(cls) -> Self:
    return cls(
        name=os.getenv("MCP_SERVER_NAME", "mcp-server"),
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", "8000")),
        debug=os.getenv("MCP_DEBUG", "false").lower() == "true",
        log_level=os.getenv("MCP_LOG_LEVEL", "INFO").upper(),
    )
```

### From Dictionary

```python
@classmethod
def from_dict(cls, config_dict: dict[str, str | int | bool]) -> Self:
    return cls(
        name=str(config_dict.get("name", "mcp-server")),
        host=str(config_dict.get("host", "0.0.0.0")),
        port=int(config_dict.get("port", 8000)),
        debug=bool(config_dict.get("debug", False)),
        log_level=str(config_dict.get("log_level", "INFO")).upper(),
    )
```

## Configuration Validation

Add validation method to check constraints:

```python
def validate(self) -> None:
    if not 1 <= self.port <= 65535:
        msg = f"Port must be between 1 and 65535, got {self.port}"
        raise ValueError(msg)
    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if self.log_level not in valid_log_levels:
        msg = f"Invalid log level: {self.log_level}"
        raise ValueError(msg)
```

## Usage in Server Factory

```python
def create_server(config: ServerConfig | None = None) -> FastMCP:
    config = config or ServerConfig.from_env()
    config.validate()
    server = FastMCP(config.name)
    return server
```

## Environment Variables

Standard environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MCP_SERVER_NAME` | str | "mcp-server" | Server name |
| `MCP_HOST` | str | "0.0.0.0" | Host to bind to |
| `MCP_PORT` | int | 8000 | Port to listen on |
| `MCP_DEBUG` | bool | false | Enable debug mode |
| `MCP_LOG_LEVEL` | str | "INFO" | Logging level |

## Best Practices

- MUST use frozen dataclasses for immutable configuration
- MUST provide sensible defaults
- MUST validate configuration before use
- SHOULD support multiple configuration sources
- SHOULD use factory methods (`from_env`, `from_dict`)
- SHOULD use type hints for all configuration fields

## Related

- @.agents/docs/conventions/coding-style.md - Dataclass patterns
- @.agents/docs/patterns/typing.md - Type hints
- @src/mcp_server/config.py - Configuration implementation
