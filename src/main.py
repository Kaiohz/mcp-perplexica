"""MCP server main entry point."""

from config import Settings
from dependencies import mcp

settings = Settings()

if __name__ == "__main__":
    mcp.run(transport=settings.transport)