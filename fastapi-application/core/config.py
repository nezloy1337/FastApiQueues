from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 50000


class ErrorDescription(BaseModel):
    conflict_description: str
    no_entry_description: str
    unknown_error_description: str


class ApiV1Prefix(BaseModel):
    prefix: str = "/convert"


class Redis(BaseModel):
    url: str = "redis://localhost:6379"
    decode_responses: bool = True
    lifetime_seconds: int = 60 * 60 * 24  # сутки


class UserManager(BaseModel):
    reset_password_token_secret: str
    verification_token_secret: str


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


class CORSConfig(BaseModel):
    origins: list[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:8080",
    ]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.templates", ".env"),  # следующий переопределяет предыдущий
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    redis: Redis = Redis()
    user_manager: UserManager
    cors: CORSConfig = CORSConfig()
    errors_description: ErrorDescription


settings = Settings()
