from typing import Generic, Optional, List, Dict, Any
from typing import Type

from sqlalchemy import update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import TModels
from utils.condition_builder import ConditionBuilder


class BaseRepository(Generic[TModels]):
    def __init__(self, model: Type[TModels], session: AsyncSession):
        self.model = model
        self.session = session
        self.condition_builder = ConditionBuilder(model)
        self.column_names = model.__table__.columns


    async def create(self, obj_data: dict) -> TModels:
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj


    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        return await self.session.get(self.model, obj_id)


    async def get_all(self) -> List[TModels]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()


    async def delete(self, **conditions: dict) -> bool:
        query_conditions = self.condition_builder.create_conditions(**conditions)
        query = delete(self.model).filter(and_(*query_conditions))
        result = await self.session.execute(query)

        if result.rowcount:
            await self.session.commit()
            return True


    async def patch(self, obj_unique_key: Dict[str, Any], **values: Any) -> Optional[Dict[str, Any]]:
        """Обновляет объект с указанным уникальным ключом."""
        try:
            # Создаём условия для фильтрации
            if filters := self.condition_builder.create_conditions(**obj_unique_key):
                # Формируем запрос на обновление
                query = (
                    update(self.model)
                    .where(*filters)  # Применяем фильтры
                    .values(**values)  # Обновляем значения
                )

                result = await self.session.execute(query)

                if result.rowcount == 0:
                    # Подтверждаем транзакцию
                    await self.session.commit()
                    return values

        except Exception as e:
            raise e








