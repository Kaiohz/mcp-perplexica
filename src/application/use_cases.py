"""Application use cases - Business logic orchestration."""

from application.requests import SearchRequestDTO
from domain.entities import (
    ChatModel,
    EmbeddingModel,
    FocusMode,
    HistoryEntry,
    OptimizationMode,
    SearchRequest,
    SearchResult,
)
from domain.ports import SearchPort


class SearchUseCase:
    """Use case for executing search operations.

    This use case orchestrates the search flow by:
    1. Receiving a validated SearchRequestDTO
    2. Transforming to domain SearchRequest
    3. Delegating to the SearchPort for execution
    4. Returning the SearchResult

    Attributes:
        _search_port: The port implementation for search operations.
    """

    def __init__(self, search_port: SearchPort) -> None:
        """Initialize SearchUseCase.

        Args:
            search_port: The port implementation for search operations.
        """
        self._search_port = search_port

    async def execute(self, request_dto: SearchRequestDTO) -> SearchResult:
        """Execute a search operation.

        Args:
            request_dto: The validated search request DTO.

        Returns:
            SearchResult containing the response and sources.

        Raises:
            SearchError: If the search operation fails.
        """
        # Direct transformations from DTO to domain entities
        chat_model = ChatModel(**request_dto.chat_model.model_dump(by_alias=False))
        embedding_model = EmbeddingModel(
            **request_dto.embedding_model.model_dump(by_alias=False)
        )
        history_entries = tuple(
            HistoryEntry(role=entry[0], content=entry[1])
            for entry in request_dto.history
        )

        request = SearchRequest(
            query=request_dto.query,
            chat_model=chat_model,
            embedding_model=embedding_model,
            focus_mode=FocusMode(request_dto.focus_mode),
            optimization_mode=OptimizationMode(request_dto.optimization_mode),
            history=history_entries,
            system_instructions=request_dto.system_instructions,
            stream=request_dto.stream,
        )

        return await self._search_port.search(request)
