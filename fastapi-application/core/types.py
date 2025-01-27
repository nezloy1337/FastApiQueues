from typing import TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:
    from domains.queues import (
        QueueEntriesRepository,
        QueueRepository,
        QueueTagsRepository,
    )  # noqa: F401
    from domains.tags import TagsRepository  # noqa: F401
    from domains.users import UserRepository  # noqa: F401

    from core.base import Base, BaseService  # noqa: F401

TRepositories = TypeVar(
    "TRepositories",
    bound=Union[
        "QueueRepository",
        "TagsRepository",
        "QueueTagsRepository",
        "QueueEntriesRepository",
        "UserRepository",
    ],
)


TService = TypeVar("TService", bound="BaseService")

TModels = TypeVar(
    "TModels",
    bound="Base",
)
