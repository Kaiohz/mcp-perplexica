"""Perplexica adapter - HTTP client implementation of SearchPort."""

from typing import Any

import httpx

from domain.entities import SearchRequest, SearchResult, Source
from domain.ports import SearchError, SearchPort


class PerplexicaAdapter(SearchPort):
    """HTTP client adapter for Perplexica search API.

    This adapter implements the SearchPort interface by making HTTP
    requests to the Perplexica API.

    Attributes:
        _base_url: Base URL of the Perplexica API.
        _client: HTTP client for making requests.
        _timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 120.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize PerplexicaAdapter.

        Args:
            base_url: Base URL of the Perplexica API (e.g., 'http://localhost:3000').
            timeout: Request timeout in seconds.
            client: Optional pre-configured HTTP client.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client = client

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client.

        Returns:
            Configured HTTP client.
        """
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    def _build_request_payload(self, request: SearchRequest) -> dict[str, Any]:
        """Build the request payload for Perplexica API.

        Args:
            request: The domain search request.

        Returns:
            Dictionary payload matching Perplexica API format.
        """
        payload: dict[str, Any] = {
            "chatModel": {
                "providerId": request.chat_model.provider_id,
                "key": request.chat_model.key,
            },
            "embeddingModel": {
                "providerId": request.embedding_model.provider_id,
                "key": request.embedding_model.key,
            },
            "optimizationMode": request.optimization_mode.value,
            "focusMode": request.focus_mode.value,
            "query": request.query,
            "history": [
                [entry.role, entry.content] for entry in request.history
            ],
            "stream": request.stream,
        }

        if request.system_instructions is not None:
            payload["systemInstructions"] = request.system_instructions

        return payload

    def _parse_response(self, data: dict[str, Any]) -> SearchResult:
        """Parse Perplexica API response into domain entity.

        Args:
            data: Raw response data from Perplexica API.

        Returns:
            SearchResult domain entity.
        """
        message = data.get("message", "")

        sources_data = data.get("sources", [])
        sources = tuple(
            Source(
                title=source.get("title", ""),
                url=source.get("url", ""),
                snippet=source.get("snippet"),
            )
            for source in sources_data
        )

        return SearchResult(message=message, sources=sources)

    async def search(self, request: SearchRequest) -> SearchResult:
        """Execute a search request against Perplexica API.

        Args:
            request: The search request containing query and configuration.

        Returns:
            SearchResult containing the response message and sources.

        Raises:
            SearchError: If the search operation fails.
        """
        client = await self._get_client()
        url = f"{self._base_url}/api/search"
        payload = self._build_request_payload(request)

        try:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)

        except httpx.HTTPStatusError as e:
            raise SearchError(
                message=f"Perplexica API returned error: {e.response.status_code}",
                cause=e,
            ) from e
        except httpx.RequestError as e:
            raise SearchError(
                message=f"Failed to connect to Perplexica API: {e}",
                cause=e,
            ) from e
        except Exception as e:
            raise SearchError(
                message=f"Unexpected error during search: {e}",
                cause=e,
            ) from e

    async def close(self) -> None:
        """Close the HTTP client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
