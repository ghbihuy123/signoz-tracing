# Signoz Tracing Project

## Components

- **Docling Celery worker**: Handles background computation tasks using Celery.
- **RabbitMQ queue**: Message broker for task distribution.
- **FastAPI**: Provides the HTTP API for computation.
- **Signoz as tracing server**: Collects and visualizes distributed tracing data.
- **Docker deployment**: All components are containerized for easy orchestration.

## Docker Images

- `ghbihuy123/docling-worker`
- `ghbihuy123/docling-fastapi`

## Development Setup

### Prerequisites

- Docker
- Docker Compose
- [Just](https://just.systems/) (optional, for running recipes)

### Running the Stack

To start all services for a specific environment (e.g., `dev`):

```sh
docker compose --env-file .env.dev -f compose.yml up --build
```
Or using Just:

```sh
just up dev
```

#### Services
- `computer-api`: FastAPI app, exposed on port 8001 (maps to container port 8000).
- `computer-worker`: Celery worker for background tasks.
- `RabbitMQ`: Defined in rabbitmq/compose.yml.
- `Signoz`: Tracing backend (see signoz-deploy/).

### Environment Variables
See services/share-libs/astrotel/README.md for OpenTelemetry configuration:

- `OTEL_SERVICE_NAME`
- `OTEL_DEPLOYMENT_ENVIRONMENT`
- `OTEL_MODE (grpc or http)`
- `OTEL_GRPC_ENDPOINT`

- `OTEL_HTTP_ENDPOINT`

## Building Individual Services
### From the services directory:

```sh
just build api
just build worker
```

## Running Locally
### From the services directory:

```sh
just run-api
just run-worker
```
## Shared Libraries
`services/share-libs/astrotel`: Contains OpenTelemetry integration and configuration.

## Testing
Each service may provide a Makefile with lint and (placeholder) unittest targets.

For more details, see the individual READMEs in each service directory.