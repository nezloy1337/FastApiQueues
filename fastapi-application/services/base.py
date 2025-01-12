# services/base_service.py
from typing import Generic, TypeVar, List, Optional
from repositories.base import BaseRepository

T = TypeVar("T")  # Тип объекта (модель SQLAlchemy)

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
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
