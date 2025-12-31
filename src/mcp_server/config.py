from dataclasses import dataclass
import os
from typing import Self


@dataclass(frozen=True)
class ServerConfig:
    name: str = "mcp-server"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            name=os.getenv("MCP_SERVER_NAME", "mcp-server"),
            host=os.getenv("MCP_HOST", "0.0.0.0"),
            port=int(os.getenv("MCP_PORT", "8000")),
            debug=os.getenv("MCP_DEBUG", "false").lower() == "true",
            log_level=os.getenv("MCP_LOG_LEVEL", "INFO").upper(),
        )

    @classmethod
    def from_dict(cls, config_dict: dict[str, str | int | bool]) -> Self:
        return cls(
            name=str(config_dict.get("name", "mcp-server")),
            host=str(config_dict.get("host", "0.0.0.0")),
            port=int(config_dict.get("port", 8000)),
            debug=bool(config_dict.get("debug", False)),
            log_level=str(config_dict.get("log_level", "INFO")).upper(),
        )

    def validate(self) -> None:
        if not 1 <= self.port <= 65535:
            msg = f"Port must be between 1 and 65535, got {self.port}"
            raise ValueError(msg)
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level not in valid_log_levels:
            msg = f"Invalid log level: {self.log_level}"
            raise ValueError(msg)
