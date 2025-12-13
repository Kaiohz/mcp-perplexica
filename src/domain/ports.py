"""Domain ports - Abstract interfaces (ABC) for external dependencies."""

from abc import ABC, abstractmethod

from src.domain.entities import SearchRequest, SearchResult


class SearchPort(ABC):
    """Port for search operations.

    This interface defines the contract for any search service adapter.
    Implementations can use different search backends (Perplexica, etc.).
    """

    @abstractmethod
    async def search(self, request: SearchRequest) -> SearchResult:
        """Execute a search request.

        Args:
            request: The search request containing query and configuration.

        Returns:
            SearchResult containing the response message and sources.

        Raises:
            SearchError: If the search operation fails.
        """
        ...


class SearchError(Exception):
    """Base exception for search-related errors.

    Attributes:
        message: Human-readable error message.
        cause: Optional underlying exception that caused this error.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        """Initialize SearchError.

        Args:
            message: Human-readable error message.
            cause: Optional underlying exception.
        """
        super().__init__(message)
        self.message = message
        self.cause = cause
