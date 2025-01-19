from typing import TypeVar

from .model import Base
from .repository import BaseRepository
from .services import BaseService

TService = TypeVar(
    "TService",
    bound=BaseService,
)

TRepositories = TypeVar(
    "TRepositories",
    bound=BaseRepository,
)

TModels = TypeVar(
    "TModels",
    bound=Base,
)
