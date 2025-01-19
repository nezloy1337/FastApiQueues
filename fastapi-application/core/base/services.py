from typing import List, Optional, Generic, TypeVar

from fastapi import HTTPException, status

from core.base import TModels
from core.base.repository import BaseRepository
from utils.exception_handlers import handle_exception


class BaseService(Generic[TModels]):
    def __init__(
        self,
        repository: BaseRepository[TModels],
    ):
        self.repository = repository

    @handle_exception
    async def create(self, obj_data: dict) -> TModels:
        return await self.repository.create(obj_data)

    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> List[TModels]:
        return await self.repository.get_all()

    async def delete(self, **conditions) -> bool:
        if await self.repository.delete(**conditions):
            return True
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")

    async def patch(self, filters, **values) -> dict:
        try:
            if data := await self.repository.patch({**filters}, **values):
                return data
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found"
            )
        except Exception as e:
            raise

TService = TypeVar(
    "TService",
    bound=BaseService,
)