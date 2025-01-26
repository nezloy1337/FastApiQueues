from typing import Dict, Tuple, Type

from core.types import TRepositories, TService, TModels
from domains.queues import (
    QueueService,
    QueueEntries,
    QueueEntriesRepository,
    QueueEntryService,
    QueueRepository,
    Queue,
    QueueTags,
    QueueTagService,
    QueueTagsRepository,
)
from domains.tags import Tags, TagsService, TagsRepository
from domains.users import User, UserService, UserRepository

MODEL_REGISTRY: Dict[
    Type[TModels],
    Tuple[
        Type[TService], Type[TRepositories]
    ],  # Значение: ( ServiceClass,RepoClass,)
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
