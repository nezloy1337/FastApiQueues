from datetime import datetime
from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar, Union  # noqa: F401

from bson import ObjectId

if TYPE_CHECKING:
    from core.base import Base, BaseRepository, BaseService  # noqa: F401
    from domains.queues import (  # noqa: F401
        QueueEntriesRepository,  # noqa: F401
        QueueEntryService,
        # noqa: F401
        QueueRepository,  # noqa: F401
        QueueService,
        QueueTagService,
        QueueTagsRepository,
    )  # noqa: F401
    from domains.tags import TagsRepository, TagsService  # noqa: F401
    from domains.users import UserRepository, UserService  # noqa: F401


JSONSerializable: TypeAlias = Union[
    str, int, float, bool, list, dict, None, datetime, ObjectId
]
MongoDocument = dict[str, JSONSerializable]
TRepositories = TypeVar(  # ошибка unbound
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
