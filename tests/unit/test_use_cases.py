"""Unit tests for use cases."""

import pytest

from application.requests import (
    ChatModelRequest,
    EmbeddingModelRequest,
    SearchRequestDTO,
)
from application.use_cases import SearchUseCase
from domain.entities import FocusMode, OptimizationMode, SearchResult, Source
from domain.ports import SearchError
from tests.doubles.search_port_double import SearchPortDouble


class TestSearchUseCase:
    """Tests for SearchUseCase."""

    @pytest.fixture
    def search_port_double(self) -> SearchPortDouble:
        """Create a search port double."""
        return SearchPortDouble()

    @pytest.fixture
    def use_case(self, search_port_double: SearchPortDouble) -> SearchUseCase:
        """Create a use case with search port double."""
        return SearchUseCase(search_port=search_port_double)

    @pytest.fixture
    def minimal_request(self) -> SearchRequestDTO:
        """Create a minimal search request DTO."""
        return SearchRequestDTO(
            query="test query",
            chatModel=ChatModelRequest(providerId="provider-1", key="test/chat-model"),
            embeddingModel=EmbeddingModelRequest(
                providerId="provider-2", key="test/embed-model"
            ),
        )

    async def test_execute_minimal_params(
        self,
        use_case: SearchUseCase,
        search_port_double: SearchPortDouble,
        minimal_request: SearchRequestDTO,
    ) -> None:
        """Should execute search with minimal parameters."""
        result = await use_case.execute(minimal_request)

        search_port_double.assert_called_once()
        assert result.message == "Test response"

    async def test_execute_builds_correct_request(
        self,
        use_case: SearchUseCase,
        search_port_double: SearchPortDouble,
    ) -> None:
        """Should build SearchRequest with correct values."""
        request_dto = SearchRequestDTO(
            query="my search query",
            chatModel=ChatModelRequest(providerId="chat-provider", key="anthropic/claude"),
            embeddingModel=EmbeddingModelRequest(
                providerId="embed-provider", key="openai/embedding"
            ),
            focusMode="academicSearch",
            optimizationMode="quality",
            systemInstructions="Be helpful",
        )

        await use_case.execute(request_dto)

        request = search_port_double.calls[0]
        assert request.query == "my search query"
        assert request.chat_model.provider_id == "chat-provider"
        assert request.chat_model.key == "anthropic/claude"
        assert request.embedding_model.provider_id == "embed-provider"
        assert request.embedding_model.key == "openai/embedding"
        assert request.focus_mode == FocusMode.ACADEMIC_SEARCH
        assert request.optimization_mode == OptimizationMode.QUALITY
        assert request.system_instructions == "Be helpful"

    async def test_execute_with_history(
        self,
        use_case: SearchUseCase,
        search_port_double: SearchPortDouble,
    ) -> None:
        """Should include conversation history in request."""
        request_dto = SearchRequestDTO(
            query="test",
            chatModel=ChatModelRequest(providerId="p1", key="m1"),
            embeddingModel=EmbeddingModelRequest(providerId="p2", key="m2"),
            history=[["human", "Hi"], ["assistant", "Hello!"]],
        )

        await use_case.execute(request_dto)

        request = search_port_double.calls[0]
        assert len(request.history) == 2
        assert request.history[0].role == "human"
        assert request.history[0].content == "Hi"
        assert request.history[1].role == "assistant"

    async def test_execute_returns_search_result(
        self,
        search_port_double: SearchPortDouble,
    ) -> None:
        """Should return SearchResult from port."""
        expected_result = SearchResult(
            message="Custom response",
            sources=(
                Source(title="Custom Source", url="https://custom.com"),
            ),
        )
        search_port_double.response = expected_result
        use_case = SearchUseCase(search_port=search_port_double)

        request_dto = SearchRequestDTO(
            query="test",
            chatModel=ChatModelRequest(providerId="p1", key="m1"),
            embeddingModel=EmbeddingModelRequest(providerId="p2", key="m2"),
        )

        result = await use_case.execute(request_dto)

        assert result.message == "Custom response"
        assert len(result.sources) == 1
        assert result.sources[0].title == "Custom Source"

    async def test_execute_propagates_error(
        self,
        search_port_double: SearchPortDouble,
    ) -> None:
        """Should propagate SearchError from port."""
        search_port_double.error = SearchError(message="Search failed")
        use_case = SearchUseCase(search_port=search_port_double)

        request_dto = SearchRequestDTO(
            query="test",
            chatModel=ChatModelRequest(providerId="p1", key="m1"),
            embeddingModel=EmbeddingModelRequest(providerId="p2", key="m2"),
        )

        with pytest.raises(SearchError) as exc_info:
            await use_case.execute(request_dto)

        assert "Search failed" in str(exc_info.value)
