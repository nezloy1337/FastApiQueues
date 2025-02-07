import os
from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

current_path = Path(__file__).resolve()
BASE_DIR = current_path.parents[2]
ENV_FILES = (os.path.join(BASE_DIR, ".env.templates"), os.path.join(BASE_DIR, ".env"))


class RunConfig(BaseModel):
    """
    Configuration for running the application.

    Attributes:
        host (str): The host address where the application will run.
        port (int): The port number for the application.
        workers (int): The number of worker processes.
    """

    host: str = "0.0.0.0"
    port: int = 50000
    workers: int = 2


class GunicornConfig(BaseModel):
    """
    Gunicorn server configuration.

    Attributes:
        host (str): The host address where Gunicorn will run.
        port (int): The port number for the Gunicorn server.
        workers (int): Number of Gunicorn worker processes.
        timeout (int): Timeout for worker processes (in seconds).
    """

    host: str = "0.0.0.0"
    port: int = 50000
    workers: int = 2
    timeout: int = 900


class ApiV1Prefix(BaseModel):
    """
    API version prefix configuration.

    Attributes:
        prefix (str): The prefix for API version 1 endpoints.
    """

    prefix: str = "/api_v1"


class Redis(BaseModel):
    """
    Redis configuration settings.

    Attributes:
        url (str): Redis connection URL.
        decode_responses (bool): Whether to decode responses from Redis.
        lifetime_seconds (int): Default expiration time for Redis keys (in seconds).
    """

    url: str = "redis://localhost:6379"
    decode_responses: bool = True
    lifetime_seconds: int = 60 * 60 * 24  # сутки


class UserManager(BaseModel):
    """
    User manager configuration for authentication.

    Attributes:
        reset_password_token_secret (str): Secret key for password reset tokens.
        verification_token_secret (str): Secret key for verification tokens.
    """

    reset_password_token_secret: str
    verification_token_secret: str


class DatabaseConfig(BaseModel):
    """
    Database connection settings.

    Attributes:
        url (PostgresDsn): The database connection URL.
        echo (bool): Whether to log SQL statements.
        echo_pool (bool): Whether to log connection pool activity.
        max_overflow (int): Maximum number of overflow connections.
        pool_size (int): Maximum number of persistent connections.
        naming_conventions (dict[str, str]):
        SQLAlchemy naming conventions for schema objects.
    """

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
    """
    Cross-Origin Resource Sharing (CORS) settings.

    Attributes:
        origins (list[str]): Allowed origins for CORS requests.
    """

    origins: list[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:8080",
    ]


class MongoConfig(BaseModel):
    """
    MongoDB connection settings.

    Attributes:
        url (str): The MongoDB connection URL.
        db_name (str): The database name in MongoDB.
    """

    url: str
    db_name: str


class CeleryConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    """
    Application-wide settings loaded from environment variables and `.env` files.

    Attributes:
        db (DatabaseConfig): Database configuration.
        user_manager (UserManager): User manager settings.
        mongo (MongoConfig): MongoDB configuration.
        redis (Redis): Redis configuration.
        cors (CORSConfig): CORS settings.
        run (RunConfig): Application runtime settings.
        gunicorn (GunicornConfig): Gunicorn server settings.
        api_v1 (ApiV1Prefix): API versioning settings.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    db: DatabaseConfig = Field(...)
    user_manager: UserManager = Field(...)
    mongo: MongoConfig = Field(...)
    celery: CeleryConfig = Field(...)
    redis: Redis = Redis()
    cors: CORSConfig = CORSConfig()
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    api_v1: ApiV1Prefix = ApiV1Prefix()


settings = Settings()
