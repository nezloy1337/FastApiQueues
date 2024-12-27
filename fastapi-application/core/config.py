from typing import Dict

from pydantic import BaseModel, ConfigDict
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 50000


class ApiV1Prefix(BaseModel):
    prefix: str = "/convert"

class Redis(BaseModel):
    url: str = "redis://localhost:6379"
    decode_responses: bool = True
    lifetime_seconds:int = 60 * 60

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10

    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.templates", ".env"),  # следующий переопределяет предыдущий
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    redis: Redis()


settings = Settings()
