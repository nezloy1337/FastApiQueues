from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """
    Abstract base model for SQLAlchemy ORM.

    This class serves as the foundation for all database models,
    providing a consistent metadata configuration.

    Attributes:
        metadata (MetaData): Defines naming conventions for database schema objects.
    """

    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_conventions)
