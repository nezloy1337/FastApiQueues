from typing import Generic, Type

from core.types import TModels, TRepositories, TService
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


class ModelRegistry(Generic[TModels, TService, TRepositories]):
    def __init__(self) -> None:
        self.MODEL_REGISTRY: dict[
            Type[TModels],
            tuple[Type[TService], Type[TRepositories]],
        ] = {}

    def register(
        self,
        model: Type[TModels],
        service_repo: tuple[Type[TService], Type[TRepositories]],
    ) -> None:
        self.MODEL_REGISTRY[model] = service_repo


model_registry: ModelRegistry[TModels, TService, TRepositories] = ModelRegistry()
model_registry.register(Queue, (QueueService, QueueRepository))
model_registry.register(QueueEntries, (QueueEntryService, QueueEntriesRepository))
model_registry.register(QueueTags, (QueueTagService, QueueTagsRepository))
model_registry.register(Tags, (TagsService, TagsRepository))
model_registry.register(User, (UserService, UserRepository))
