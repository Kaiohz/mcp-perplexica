"""Domain entities - Pure Python dataclasses representing business concepts."""

from dataclasses import dataclass, field
from enum import StrEnum


class FocusMode(StrEnum):
    """Search focus modes available in Perplexica."""

    WEB_SEARCH = "webSearch"
    ACADEMIC_SEARCH = "academicSearch"
    WRITING_ASSISTANT = "writingAssistant"
    WOLFRAM_ALPHA = "wolframAlphaSearch"
    YOUTUBE_SEARCH = "youtubeSearch"
    REDDIT_SEARCH = "redditSearch"


class OptimizationMode(StrEnum):
    """Search optimization modes available in Perplexica."""

    SPEED = "speed"
    BALANCED = "balanced"
    QUALITY = "quality"


@dataclass(frozen=True)
class ChatModel:
    """Configuration for the chat model used in search.

    Attributes:
        provider_id: Unique identifier for the model provider.
        key: Model key in format 'provider/model-name'.
    """

    provider_id: str
    key: str


@dataclass(frozen=True)
class EmbeddingModel:
    """Configuration for the embedding model used in search.

    Attributes:
        provider_id: Unique identifier for the model provider.
        key: Model key in format 'provider/model-name'.
    """

    provider_id: str
    key: str


@dataclass(frozen=True)
class HistoryEntry:
    """A single entry in conversation history.

    Attributes:
        role: The role of the message sender ('human' or 'assistant').
        content: The message content.
    """

    role: str
    content: str


@dataclass(frozen=True)
class SearchRequest:
    """Request to perform a search through Perplexica.

    Attributes:
        query: The search query string.
        chat_model: Configuration for the chat model.
        embedding_model: Configuration for the embedding model.
        focus_mode: The search focus mode.
        optimization_mode: The optimization mode for search.
        history: Conversation history for context.
        system_instructions: Optional custom system instructions.
        stream: Whether to stream the response.
    """

    query: str
    chat_model: ChatModel
    embedding_model: EmbeddingModel
    focus_mode: FocusMode = FocusMode.WEB_SEARCH
    optimization_mode: OptimizationMode = OptimizationMode.BALANCED
    history: tuple[HistoryEntry, ...] = field(default_factory=tuple)
    system_instructions: str | None = None
    stream: bool = False


@dataclass(frozen=True)
class Source:
    """A source reference from search results.

    Attributes:
        title: Title of the source.
        url: URL of the source.
        snippet: Optional snippet from the source content.
    """

    title: str
    url: str
    snippet: str | None = None


@dataclass(frozen=True)
class SearchResult:
    """Result from a Perplexica search.

    Attributes:
        message: The generated response message.
        sources: List of sources used to generate the response.
    """

    message: str
    sources: tuple[Source, ...] = field(default_factory=tuple)
