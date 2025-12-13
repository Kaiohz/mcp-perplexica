"""Application requests - Pydantic DTOs for input validation."""

from pydantic import BaseModel, ConfigDict, Field


class ChatModelRequest(BaseModel):
    """Request DTO for chat model configuration.

    Attributes:
        provider_id: Unique identifier for the model provider.
        key: Model key in format 'provider/model-name'.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "provider_id": "a1850332-621f-4960-b005-b005b8680328",
                "key": "anthropic/claude-sonnet-4.5",
            }
        }
    )

    provider_id: str = Field(..., alias="providerId", min_length=1)
    key: str = Field(..., min_length=1)


class EmbeddingModelRequest(BaseModel):
    """Request DTO for embedding model configuration.

    Attributes:
        provider_id: Unique identifier for the model provider.
        key: Model key in format 'provider/model-name'.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "provider_id": "a1850332-621f-4960-b005-b005b8680328",
                "key": "openai/text-embedding-3-small",
            }
        }
    )

    provider_id: str = Field(..., alias="providerId", min_length=1)
    key: str = Field(..., min_length=1)


class SearchRequestDTO(BaseModel):
    """Request DTO for search operations.

    Attributes:
        query: The search query string.
        chat_model: Configuration for the chat model.
        embedding_model: Configuration for the embedding model.
        focus_mode: The search focus mode.
        optimization_mode: The optimization mode for search.
        history: Conversation history as list of [role, content] tuples.
        system_instructions: Optional custom system instructions.
        stream: Whether to stream the response.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "What is the capital of France?",
                "chatModel": {
                    "providerId": "a1850332-621f-4960-b005-b005b8680328",
                    "key": "anthropic/claude-sonnet-4.5",
                },
                "embeddingModel": {
                    "providerId": "a1850332-621f-4960-b005-b005b8680328",
                    "key": "openai/text-embedding-3-small",
                },
                "focusMode": "webSearch",
                "optimizationMode": "balanced",
                "history": [
                    ["human", "Hi, how are you?"],
                    ["assistant", "I am doing well, how can I help you today?"],
                ],
                "systemInstructions": "Focus on providing accurate information",
                "stream": False,
            }
        }
    )

    query: str = Field(..., min_length=1, description="The search query string")
    chat_model: ChatModelRequest = Field(..., alias="chatModel")
    embedding_model: EmbeddingModelRequest = Field(..., alias="embeddingModel")
    focus_mode: str = Field(
        default="webSearch",
        alias="focusMode",
        description="Search focus mode",
    )
    optimization_mode: str = Field(
        default="balanced",
        alias="optimizationMode",
        description="Optimization mode for search",
    )
    history: list[list[str]] = Field(
        default_factory=list,
        description="Conversation history as list of [role, content] pairs",
    )
    system_instructions: str | None = Field(
        default=None,
        alias="systemInstructions",
        description="Custom system instructions",
    )
    stream: bool = Field(default=False, description="Whether to stream the response")
