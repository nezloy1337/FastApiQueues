from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from core.base import Base, BaseService  # noqa: F401
    from domains.queues import (  # noqa: F401
        QueueEntriesRepository,  # noqa: F401
        QueueRepository,  # noqa: F401
        QueueTagsRepository,  # noqa: F401
    )  # noqa: F401
    from domains.tags import TagsRepository  # noqa: F401
    from domains.users import UserRepository  # noqa: F401

TRepositories = TypeVar(  # ошибка unbound
    "TRepositories",
    "QueueRepository",
    "TagsRepository",
    "QueueTagsRepository",
    "QueueEntriesRepository",
    "UserRepository",
)


TService = TypeVar("TService", bound="BaseService")

TModels = TypeVar(
    "TModels",
    bound="Base",
)
