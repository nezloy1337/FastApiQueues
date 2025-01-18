from typing import TypeVar, Union

from . import BaseService

TService = TypeVar(
    "TService",
    bound=Union[
        BaseService
    ],
)
