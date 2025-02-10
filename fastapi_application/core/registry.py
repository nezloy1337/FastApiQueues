from typing import Type

from core.base import Base
from core.types import TRepositories, TService
from domains.queues import (
    Queue,
    QueueEntries,
    QueueEntriesRepository,
    QueueEntryService,
    QueueRepository,
    QueueService,
    QueueTags,
    QueueTagService,
    QueueTagsRepository,
)
from domains.tags import Tags, TagsRepository, TagsService
from domains.users import User, UserRepository, UserService

MODEL_REGISTRY: dict[
    Type[Base],
    tuple[Type[TService], Type[TRepositories]],  # Значение: ( ServiceClass,RepoClass,)
] = {
    Queue: (
        QueueService,
        QueueRepository,
    ),
    QueueEntries: (
        QueueEntryService,
        QueueEntriesRepository,
    ),
    QueueTags: (
        QueueTagService,
        QueueTagsRepository,
    ),
    Tags: (
        TagsService,
        TagsRepository,
    ),
    User: (
        UserService,
        UserRepository,
    ),
}
