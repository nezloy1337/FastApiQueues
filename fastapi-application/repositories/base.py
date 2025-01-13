from typing import Generic, TypeVar, Type, List, Optional
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import Queue, QueueEntries, User, Tags, QueueTags

# Определяем параметр типа T, который может быть любым из указанных типов
T = TypeVar("T", bound=Union[Queue, Tags, QueueEntries, User , QueueTags])


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session


    async def create(self, obj_data: dict) -> T:
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj


    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.session.get(self.model, obj_id)


    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()


    async def delete(self, obj_id: int) -> bool:
        query = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delete failed:now data is changed",
            )
        return True

    async def update(self, obj_id: int, obj_data: dict) -> dict:
        query = update(self.model).where(self.model.id == obj_id).values(**obj_data)
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update failed: no data is changed",
            )
        await self.session.commit()
        return obj_data
