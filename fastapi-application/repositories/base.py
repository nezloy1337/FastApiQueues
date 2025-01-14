from typing import Generic, Type, List, Optional

from sqlalchemy import update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models.types import T
from utils.condition_builder import ConditionBuilder


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session
        self.condition_builder = ConditionBuilder(model)


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


    async def delete(self, **conditions: dict) -> bool:
        query_conditions = self.condition_builder.create_condition(**conditions)
        query = delete(self.model).where(and_(*query_conditions))
        result = await self.session.execute(query)

        if result.rowcount:
            await self.session.commit()
            return True

    async def update(self, obj_id, **values) -> dict:
        query = update(self.model).where(self.model.id == obj_id).values(**values)
        result = await self.session.execute(query)
        if result.rowcount:
            await self.session.commit()
            return values
