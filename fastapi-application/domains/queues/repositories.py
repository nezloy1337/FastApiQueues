from typing import Any

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.base.repository import BaseRepository
from domains.queues import Queue, QueueEntries, QueueTags
from utils.condition_builder import ConditionBuilder
from utils.exceptions import DuplicateEntryError

"""
отдельный файл для каждого репозитория для дальнейшего маштабирования и развития проекта
"""


class QueueRepository(BaseRepository[Queue]):
    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            Queue,
            session,
            condition_builder,
        )

    async def get_by_id(self, queue_id: int) -> Queue | None:
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

    async def get_all(self) -> list[Queue]:
        query = select(Queue).options(
            selectinload(Queue.queue_tags),
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


class QueueEntriesRepository(BaseRepository[QueueEntries]):
    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(QueueEntries, session, condition_builder)

    async def delete_all(self, filters: dict[str, Any]) -> QueueEntries | None:
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

    async def create(self, obj_data: dict[str, Any]) -> QueueEntries:
        """
        Создаёт новый объект на основе переданных данных и сохраняет его в базе данных.

        :param obj_data: Словарь с данными для создания записи.
        :return: Созданный экземпляр модели.
        """
        filters = self.condition_builder.create_conditions(
            user_id=obj_data.get("user_id"),
            queue_id=obj_data.get("queue_id"),
        )

        queue_entry = await self.session.execute(select(self.model).filter(*filters))
        if queue_entry.scalar_one_or_none():
            raise DuplicateEntryError

        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()

        return obj


class QueueTagsRepository(BaseRepository[QueueTags]):
    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            QueueTags,
            session,
            condition_builder,
        )
