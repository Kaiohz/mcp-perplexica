"""Dependency injection - Factory functions for application components."""

from application.use_cases import SearchUseCase
from config import Settings
from infrastructure.perplexica.adapter import PerplexicaAdapter
from mcp.server.fastmcp import FastMCP

settings = Settings()

# Create MCP server
mcp = FastMCP(
    name="mcp-perplexica",
    instructions="""
    MCP server for Perplexica search API.
    
    This server provides web search capabilities through Perplexica,
    allowing you to search the web and get AI-generated responses
    with source citations.
    
    Available tools:
    - search: Perform a web search using Perplexica
    """,
)


def get_perplexica_adapter() -> PerplexicaAdapter:
    """Create PerplexicaAdapter instance.

    Args:
        settings: Optional settings instance. If not provided, loads from environment.

    Returns:
        Configured PerplexicaAdapter instance.
    """
    return PerplexicaAdapter(
        base_url=settings.perplexica_url,
        timeout=settings.perplexica_timeout,
    )


def get_search_use_case() -> SearchUseCase:
    """Create SearchUseCase instance with dependencies.

    Args:
        settings: Optional settings instance. If not provided, loads from environment.

    Returns:
        Configured SearchUseCase instance.
    """
    adapter = get_perplexica_adapter()
    return SearchUseCase(search_port=adapter)
