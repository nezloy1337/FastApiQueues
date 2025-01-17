from typing import List, Optional, Generic

from fastapi import HTTPException, status

from models import TModels
from repositories import BaseRepository
from utils.exception_handlers import ExceptionHandler


class BaseService(Generic[TModels]):
    def __init__(self, repository: BaseRepository[TModels] , exception_handler: ExceptionHandler):
        self.repository = repository
        self.error_handler = exception_handler

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

    async def patch(self, obj_unique_ley , **values) -> dict:
        try:
            if data := await self.repository.patch({**obj_unique_ley}, **values):
                return data
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
        except Exception as e:
            self.error_handler.handle(e)



