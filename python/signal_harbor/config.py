from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SRP: configuration concerns are isolated here; no business logic lives in this class
    model_config = SettingsConfigDict(env_prefix="SIGNAL_HARBOR_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./signal_harbor.db"
    redis_url: str = "redis://localhost:6379/0"
    api_key: str = "dev-api-key"
    risk_lookback_hours: int = 24
    cache_ttl_seconds: int = 60
