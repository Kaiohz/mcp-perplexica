# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY src/ ./src/

# Install the project
RUN uv sync --frozen --no-dev


# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment and source from builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/pyproject.toml /app/pyproject.toml

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PERPLEXICA_URL=http://perplexica:3000

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import main" || exit 1

# Run MCP server
CMD ["python", "-m", "main"]
