from fastmcp import FastMCP

from mcp_server.config import ServerConfig
from mcp_server.prompts import register_prompts
from mcp_server.resources import register_resources
from mcp_server.tools import register_tools


def create_server(config: ServerConfig | None = None) -> FastMCP:
    config = config or ServerConfig.from_env()
    server = FastMCP(config.name)
    register_tools(server)
    register_resources(server)
    register_prompts(server)
    return server


mcp = create_server()


def main() -> int:
    try:
        mcp.run()
        return 0
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1


if __name__ == "__main__":
    main()
