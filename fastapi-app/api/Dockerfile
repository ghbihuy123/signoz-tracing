### Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY ./api/pyproject.toml ./api/uv.lock ./
RUN uv sync --no-dev

### Final stage
FROM python:3.12-slim AS final

WORKDIR /app

# Use /app/.venv as python environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy neccessary files
COPY --from=builder /app/.venv /app/.venv
COPY ./api /app/api
COPY ./worker /app/worker

ENTRYPOINT ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
