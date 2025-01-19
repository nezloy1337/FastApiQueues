from typing import TypeVar, Union

from repositories import BaseRepository

TRepositories = TypeVar(
    "TRepositories",
    bound=Union[
        BaseRepository,
    ],
)
