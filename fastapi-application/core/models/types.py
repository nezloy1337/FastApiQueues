from typing import TypeVar
from typing import Union

from core.models import Queue, QueueEntries, User, Tags, QueueTags

# Определяем параметр типа T, который может быть любым из указанных типов
T = TypeVar("T", bound=Union[Queue, Tags, QueueEntries, User, QueueTags])