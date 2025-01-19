from typing import Dict, Tuple, Type

from domains.queues import QueueService, QueueEntries, QueueEntriesRepository, QueueEntryService, QueueRepository, \
    Queue, QueueTags, QueueTagService, QueueTagsRepository
from domains.tags import Tags, TagsService, TagsRepository
from domains.users import User, UserService, UserRepository
from models import TModels
from repositories import BaseRepository
from services import BaseService

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
