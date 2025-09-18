from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General app config
    app_name: str = "fastapi-demo"
    app_env: str = "development"
    db_url: str

    # OTEL config
    service_name: str = "unknown-service"
    deployment_environment: str = "dev"
    mode: str = "grpc"
    grpc_endpoint: str = "http://localhost:4317"
    http_endpoint: str = "http://localhost:4318"

    class Config:
        env_file = ".env"
        env_prefix = "OTEL_" 