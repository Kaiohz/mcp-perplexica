# MCP Perplexica

MCP server proxy for [Perplexica](https://github.com/ItzCrazyKns/Perplexica) search API.

This server allows LLMs to perform web searches through Perplexica using the Model Context Protocol (MCP).

## Features

- 🔍 Web search through Perplexica
- 📚 Multiple focus modes (web, academic, YouTube, Reddit, etc.)
- ⚡ Configurable optimization modes (speed, balanced, quality)
- 🔧 Customizable model configuration
- 📖 Source citations in responses

## Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) package manager
- Running [Perplexica](https://github.com/ItzCrazyKns/Perplexica) instance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kaiohz/mcp-perplexica.git
cd mcp-perplexica
```

2. Install dependencies with UV:
```bash
uv sync
```

3. Create your environment file:
```bash
cp .env.example .env
```

4. Edit `.env` with your configuration:
```bash
PERPLEXICA_URL=http://localhost:3000
DEFAULT_CHAT_MODEL_PROVIDER_ID=your-provider-id
DEFAULT_CHAT_MODEL_KEY=anthropic/claude-sonnet-4.5
DEFAULT_EMBEDDING_MODEL_PROVIDER_ID=your-provider-id
DEFAULT_EMBEDDING_MODEL_KEY=openai/text-embedding-3-small
```

## Usage

### Running with Docker Compose

The easiest way to run both Perplexica and MCP Perplexica together:

```bash
# Copy and configure environment files
cp .env.example .env
cp .env.perplexica.example .env.perplexica

# Edit .env with your MCP Perplexica settings
# Edit .env.perplexica with your Perplexica settings

# Start services
docker compose up -d
```

This starts:
- **Perplexica** on `http://localhost:3000`
- **MCP Perplexica** connected to Perplexica

### Running the MCP Server (without Docker)

```bash
uv run mcp-perplexica
```

Or directly:
```bash
uv run python -m src.main
```

### Claude Desktop Configuration

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "perplexica": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-perplexica", "mcp-perplexica"],
      "env": {
        "PERPLEXICA_URL": "http://localhost:3000",
        "DEFAULT_CHAT_MODEL_PROVIDER_ID": "your-provider-id",
        "DEFAULT_CHAT_MODEL_KEY": "anthropic/claude-sonnet-4.5",
        "DEFAULT_EMBEDDING_MODEL_PROVIDER_ID": "your-provider-id",
        "DEFAULT_EMBEDDING_MODEL_KEY": "openai/text-embedding-3-small"
      }
    }
  }
}
```

## Available Tools

### `search`

Perform a web search using Perplexica.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The search query |
| `focus_mode` | string | No | Search focus: `webSearch`, `academicSearch`, `writingAssistant`, `wolframAlphaSearch`, `youtubeSearch`, `redditSearch` |
| `optimization_mode` | string | No | Optimization: `speed`, `balanced`, `quality` |
| `system_instructions` | string | No | Custom instructions for AI response |
| `chat_model_provider_id` | string | No | Override default chat model provider |
| `chat_model_key` | string | No | Override default chat model |
| `embedding_model_provider_id` | string | No | Override default embedding provider |
| `embedding_model_key` | string | No | Override default embedding model |

**Example:**
```
Search for "latest developments in AI" using academic focus
```

## Development

### Install dev dependencies

```bash
uv sync --dev
```

### Run tests

```bash
uv run pytest
```

### Run linter

```bash
uv run ruff check .
uv run ruff format .
uv run black src/
```

## Architecture

This project follows hexagonal architecture:

```
src/
├── main.py              # MCP server entry point
├── config.py            # Pydantic Settings
├── dependencies.py      # Dependency injection
├── domain/              # Business core (pure Python)
│   ├── entities.py      # Dataclasses
│   └── ports.py         # ABC interfaces
├── application/         # Use cases
│   ├── requests.py      # Pydantic DTOs
│   └── use_cases.py     # Business logic
└── infrastructure/      # External adapters
    └── perplexica/
        └── adapter.py   # HTTP client
```

## License

MIT
