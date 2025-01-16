from typing import TypeVar

from .base import Base as BaseModel

TModels = TypeVar(
    "TModels",
    bound=BaseModel,
)

