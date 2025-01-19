from typing import TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from utils import camel_case_to_snake_case
from core.config import settings




class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive  # позволяет вместо tablename = str сделать метод
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    metadata = MetaData(naming_convention=settings.db.naming_conventions)

TModels = TypeVar(
    "TModels",
    bound=Base,
)
