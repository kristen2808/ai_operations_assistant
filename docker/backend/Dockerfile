FROM python:3.12-slim

# Install uv via pip
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy pyproject.toml first for caching
COPY pyproject.toml /app/

# Install dependencies with uv
RUN uv sync

# Copy the entire backend app to /app/backend
COPY backend /app/backend

# Make sure __init__.py files exist to make modules importable
RUN touch /app/backend/__init__.py && touch /app/backend/app/__init__.py

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run with uv
CMD ["uv", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]