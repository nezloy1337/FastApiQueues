from typing import Generic, TypeVar, List, Optional, Union

from fastapi import HTTPException, status

from repositories.base import BaseRepository

T = TypeVar("T")  # Тип объекта (модель SQLAlchemy)


class BaseService(Generic[T]):
    def __init__(
        self, repository: Union[BaseRepository[T]]
    ):
        self.repository = repository

    async def create(self, obj_data: dict) -> T:
        return await self.repository.create(obj_data)

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> List[T]:
        return await self.repository.get_all()

    async def delete(self,**conditions)  -> bool:
        if await self.repository.delete(**conditions):
            return True
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")

    async def update(self,obj_id, **values) -> Optional[T]:
        if await self.repository.update(obj_id,**values):
            return True
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")


