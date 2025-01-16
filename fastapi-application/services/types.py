from typing import TypeVar, Union

from .services import (
    QueueService,
    QueueTagService,
    TagsService,
    QueueEntryService,
    UserService,
)

TService = TypeVar(
    "TService",
    bound=Union[
        QueueService,
        TagsService,
        QueueEntryService,
        UserService,
        QueueTagService
    ],
)
