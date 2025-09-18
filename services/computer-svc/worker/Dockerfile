### Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv (fast dependency installer)
RUN pip install uv

# Prepare folder to install
RUN mkdir /app/computer-svc && mkdir /app/computer-svc/worker

# Copy dependency files
COPY ./computer-svc/worker/pyproject.toml ./computer-svc/worker/uv.lock /app/computer-svc/worker

# Install dependencies into a venv
RUN cd /app/computer-svc/worker && \
    uv sync --no-dev

### Final stage
FROM python:3.12-slim AS final

WORKDIR /app

# Copy virtual environment
COPY --from=builder /app/computer-svc/worker/.venv /app/.venv

# Set environment variables so Python uses venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy worker source code
COPY ./computer-svc/worker ./worker

# Run Celery worker
ENTRYPOINT ["celery", "-A", "worker.celery_app.celery_app", "worker", "--loglevel=info", "-Q", "default"]
