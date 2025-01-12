from typing import Generic, TypeVar, Type, List, Optional

from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from core.models import Queue, QueueEntries, QueueTags

# Определяем параметр типа T, который может быть любым из указанных типов
T = TypeVar("T", bound=Union[Queue, QueueTags, QueueEntries])


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
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def update(self, obj_id: int, obj_data: dict) -> dict:
        query = update(self.model).where(self.model.id == obj_id).values(**obj_data)
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update failed:now data is changed",
            )
        await self.session.commit()
        return obj_data
