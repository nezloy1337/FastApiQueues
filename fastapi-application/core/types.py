from typing import TypeVar, Union, TYPE_CHECKING



if TYPE_CHECKING:
    pass

TRepositories = TypeVar(
    "TRepositories",
    bound=Union["QueueRepository "],
)


TService = TypeVar(
    "TService",
    bound="BaseService"
)


