from typing import TypeVar, Union

from .queue import Queue, QueueEntries
from .tags import Tags, QueueTags
from .user import User

TModels = TypeVar(
    "TModels",
    bound=Union[
        Queue,
        QueueEntries,
        Tags,
        User,
        QueueTags,
    ],
)
