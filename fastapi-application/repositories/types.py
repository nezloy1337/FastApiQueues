from typing import TypeVar, Union

from .queue import QueueRepository
from .queue_entry import QueueEntriesRepository
from .queue_tags import QueueTagsRepository
from .tags import TagsRepository
from .user import UserRepository

TRepositories = TypeVar(
    "TRepositories",
    bound=Union[
        TagsRepository,
        UserRepository,
        QueueTagsRepository,
        QueueRepository,
        QueueEntriesRepository,
    ],
)
