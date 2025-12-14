"""MCP server main entry point."""

from config import Settings
from dependencies import mcp

# Import api module to register MCP tools via decorators
import application.api  # noqa: F401

settings = Settings()

if __name__ == "__main__":
    mcp.run(transport=settings.transport)