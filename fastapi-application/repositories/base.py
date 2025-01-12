# repositories/base_repository.py
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")  # Тип объекта (модель SQLAlchemy)

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

    async def update(self, obj_id: int, obj_data: dict) -> Optional[T]:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None
        for key, value in obj_data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
