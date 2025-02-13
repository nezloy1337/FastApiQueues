from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar, Union  # noqa: F401

if TYPE_CHECKING:
    from core.base import Base, BaseRepository, BaseService  # noqa: F401


TRepositories = TypeVar(
    "TRepositories",
    bound="BaseRepository[Any]",
)

TService = TypeVar(
    "TService",
    bound="BaseService[Any,Any]",
)

TModels = TypeVar(
    "TModels",
    bound="Base",
)
