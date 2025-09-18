### Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

RUN mkdir /app/computer-svc && mkdir /app/computer-svc/api

COPY ./computer-svc/api/pyproject.toml ./computer-svc/api/uv.lock /app/computer-svc/api
COPY ./share-libs/otel_tracing /app/share-libs/otel_tracing
RUN cd /app/computer-svc/api && \
    uv sync --no-dev

### Final stage
FROM python:3.12-slim AS final

WORKDIR /app

# Use /app/.venv as python environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy neccessary files
COPY --from=builder /app/computer-svc/api/.venv /app/.venv
COPY ./computer-svc/api /app/api
COPY ./computer-svc/worker /app/worker

EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
