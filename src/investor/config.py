from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="INVESTOR_",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    max_query_length: int = Field(default=10_000, ge=100, le=100_000)
    max_subagents: int = Field(default=4, ge=1, le=16)
    agent_config_dir: Path = Path("config/agents")
    mcp_config_path: Path = Path("config/mcp.servers.example.json")
    web_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
