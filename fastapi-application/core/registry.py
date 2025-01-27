from typing import Type

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

from core.types import TModels, TRepositories, TService

MODEL_REGISTRY: dict[
    Type[TModels],
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
