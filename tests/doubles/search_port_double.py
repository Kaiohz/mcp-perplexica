"""Test doubles for testing."""

from domain.entities import SearchRequest, SearchResult, Source
from domain.ports import SearchError, SearchPort


class SearchPortDouble(SearchPort):
    """Test double implementation of SearchPort.

    This double allows setting up canned responses and tracking calls
    for verification in tests.

    Attributes:
        calls: List of SearchRequest objects received.
        response: The canned response to return.
        error: Optional error to raise instead of returning response.
    """

    def __init__(
        self,
        response: SearchResult | None = None,
        error: SearchError | None = None,
    ) -> None:
        """Initialize SearchPortDouble.

        Args:
            response: The canned response to return from search().
            error: Optional error to raise from search().
        """
        self.calls: list[SearchRequest] = []
        self.response = response or SearchResult(
            message="Test response",
            sources=(
                Source(
                    title="Test Source",
                    url="https://example.com",
                    snippet="Test snippet",
                ),
            ),
        )
        self.error = error

    async def search(self, request: SearchRequest) -> SearchResult:
        """Record the call and return canned response.

        Args:
            request: The search request.

        Returns:
            The canned SearchResult.

        Raises:
            SearchError: If error was configured.
        """
        self.calls.append(request)

        if self.error:
            raise self.error

        return self.response

    def assert_called_once(self) -> None:
        """Assert that search was called exactly once."""
        assert len(self.calls) == 1, f"Expected 1 call, got {len(self.calls)}"

    def assert_called_with_query(self, query: str) -> None:
        """Assert that search was called with a specific query.

        Args:
            query: The expected query string.
        """
        assert any(
            call.query == query for call in self.calls
        ), f"No call with query '{query}' found"
