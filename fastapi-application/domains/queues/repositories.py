from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.base import TModels
from core.base.repository import BaseRepository
from domains.queues import Queue, QueueEntries, QueueTags
from utils.condition_builder import ConditionBuilder

"""
отдельный файл для каждого репозитория для дальнейшего маштабирования и развития проекта
"""

class QueueRepository(BaseRepository[Queue]):
    def __init__(self, session: AsyncSession, condition_builder:ConditionBuilder):
        super().__init__(
            Queue,
            session,
            condition_builder
        )

    async def get_by_id(self, queue_id: int) -> Queue:
        query = (
            select(Queue)
            .where(Queue.id == queue_id)
            .options(
                selectinload(Queue.entries).selectinload(QueueEntries.user),
                selectinload(Queue.queue_tags),  # Загружаем связанные теги
            )
        )

        result = await self.session.execute(query)
        return result.scalars().first()


    async def get_all(self):
        query = (
            select(Queue)
            .options(
                selectinload(Queue.queue_tags),
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()

class QueueEntriesRepository(BaseRepository[QueueEntries]):
    def __init__(self,session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(QueueEntries,session,condition_builder)

    async def delete_all(self, filters: dict) -> TModels | None:
        """
        Удаляет объекты, соответствующие указанным условиям, возвращает все
        удалённые объекты.
        Если объект не найдены, возвращается None.

        :param filters: Произвольные условия для фильтрации объектов.
        :return: Удалённый объект или None, если ничего не удалено.
        """
        query_conditions = self.condition_builder.create_conditions(**filters)

        stmt = delete(self.model).filter(and_(*query_conditions)).returning(self.model)

        result = await self.session.execute(stmt)
        deleted_obj = result.scalars().first()
        if deleted_obj:
            await self.session.commit()
        return deleted_obj


class QueueTagsRepository(BaseRepository):
    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            QueueTags,
            session,
            condition_builder,
        )
