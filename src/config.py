"""Configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Google Cloud Storage settings
    gcs_project_id: str | None = None
    gcs_bucket_name: str | None = None
    google_application_credentials: str = "credentials/googlecloud/sa.json"

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # CORS settings
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ]

    # Signed URL expiration (minutes)
    signed_url_expiration_minutes: int = 60


# Global settings instance
settings = Settings()
