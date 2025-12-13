"""Application API - MCP tool definitions."""

from dependencies import mcp, get_search_use_case
from application.requests import SearchRequestDTO
from domain.ports import SearchError


@mcp.tool()
async def search(search_request: SearchRequestDTO) -> str:
    """Search the web using Perplexica and get AI-generated responses with sources.

    Args:
        search_request: The search request containing query, models, and options.

    Returns:
        A formatted string containing the AI-generated response and source citations.
    """
    use_case = get_search_use_case()

    try:
        result = await use_case.execute(search_request)

        response_parts = [result.message]

        if result.sources:
            response_parts.append("\n\n## Sources")
            for i, source in enumerate(result.sources, 1):
                source_line = f"{i}. [{source.title}]({source.url})"
                if source.snippet:
                    source_line += f"\n   > {source.snippet}"
                response_parts.append(source_line)

        return "\n".join(response_parts)

    except SearchError as e:
        return f"Search failed: {e.message}"
    except Exception as e:
        return f"Unexpected error: {e}"