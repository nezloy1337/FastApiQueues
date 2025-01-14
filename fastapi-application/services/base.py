from typing import Generic, TypeVar, List, Optional, Union, Dict
from uuid import UUID

from fastapi import HTTPException, status

from repositories.base import BaseRepository, ExtendedBaseRepository

T = TypeVar("T")  # Тип объекта (модель SQLAlchemy)


class BaseService(Generic[T]):
    def __init__(
        self, repository: Union[BaseRepository[T], ExtendedBaseRepository[T]]
    ):
        self.repository = repository

    async def create(self, obj_data: dict) -> T:
        return await self.repository.create(obj_data)

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> List[T]:
        return await self.repository.get_all()

    async def delete(self, obj_id: int) -> bool:
        return await self.repository.delete(obj_id)

    async def update(self, obj_id: int, obj_data: dict) -> Optional[T]:
        return await self.repository.update(obj_id, obj_data)


class ExtendedBaseService(BaseService[T]):
    def __init__(self, repository: ExtendedBaseRepository[T]):
        super().__init__(repository)

    async def delete_with_extra_param(self, **kwargs: Dict[str, Union[str, int, UUID]]):
        if not await self.repository.delete_with_extra_param(**kwargs):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request: nothing to delete",
            )
