### Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv (fast dependency installer)
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a venv
RUN uv sync --no-dev

### Final stage
FROM python:3.12-slim AS final

WORKDIR /app

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv

# Set environment variables so Python uses venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy worker source code
COPY . .

# Run Celery worker
ENTRYPOINT ["celery", "-A", "celery_app.celery_app", "worker", "--loglevel=info", "-Q", "default"]
