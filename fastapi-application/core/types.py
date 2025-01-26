from typing import TypeVar, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from core.base import Base, BaseService# noqa: F401
    from domains.queues import QueueTagsRepository, QueueEntriesRepository# noqa: F401
    from domains.tags import TagsRepository# noqa: F401
    from domains.users import UserRepository # noqa: F401


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
