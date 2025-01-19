from typing import Dict, Tuple, Type

from models import TModels, Queue, User, QueueEntries, QueueTags, Tags
from repositories import (
    BaseRepository,
    QueueRepository,
    UserRepository,
    QueueEntriesRepository,
    QueueTagsRepository,
    TagsRepository,
)
from services import (
    BaseService,
    QueueService,
    UserService,
    QueueEntryService,
    QueueTagService,
    TagsService,
)

MODEL_REGISTRY: Dict[
    Type[TModels],
    Tuple[
        Type[BaseService], Type[BaseRepository]
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
