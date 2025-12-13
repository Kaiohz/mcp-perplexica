"""Configuration - Pydantic Settings for application configuration."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        perplexica_url: Base URL for Perplexica API.
        perplexica_timeout: Request timeout in seconds.
        transport: Transport type for MCP server (stdio, sse, streamable-http).
        host: Host to bind the server to (for sse and streamable-http).
        port: Port to bind the server to (for sse and streamable-http).
        default_chat_model_provider_id: Default provider ID for chat model.
        default_chat_model_key: Default key for chat model.
        default_embedding_model_provider_id: Default provider ID for embedding model.
        default_embedding_model_key: Default key for embedding model.
        default_focus_mode: Default search focus mode.
        default_optimization_mode: Default optimization mode.
        default_system_instructions: Default system instructions for searches.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Perplexica API configuration
    perplexica_url: str = "http://localhost:3000"
    perplexica_timeout: float = 120.0

    # MCP Server configuration
    transport: Literal["stdio", "sse", "streamable-http"] = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000

    # Default model configuration
    default_chat_model_provider_id: str = ""
    default_chat_model_key: str = "anthropic/claude-sonnet-4.5"
    default_embedding_model_provider_id: str = ""
    default_embedding_model_key: str = "openai/text-embedding-3-small"

    # Default search configuration
    default_focus_mode: str = "webSearch"
    default_optimization_mode: str = "balanced"
    default_system_instructions: str | None = None
