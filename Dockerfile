# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install system dependencies (curl for health check, ca-certificates for HTTPS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv by copying it from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy python project metadata
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (without installing the project itself)
RUN uv sync --frozen --no-install-project

# Copy project source code and database migrations config
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Expose FastAPI default port
EXPOSE 8000

# Run uvicorn server in the virtual environment via uv run
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
