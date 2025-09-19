from typing import Literal

from pydantic_settings import BaseSettings


class AstrotelSettings(BaseSettings):
    # OTEL config
    service_name: str = "unknown-service"
    deployment_environment: str = "dev"
    mode: str = "grpc"
    grpc_endpoint: str = "http://localhost:4317"
    http_endpoint: str = "http://localhost:4318"
    logs_ship_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    class Config:
        env_file = ".env"
        env_prefix = "OTEL_"
