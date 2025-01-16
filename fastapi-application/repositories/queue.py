from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Queue, QueueEntries
from repositories.base import BaseRepository

"""
отдельный файл для каждого репозитория для дальнейшего маштабирования и развития проекта
"""

class QueueRepository(BaseRepository[Queue]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            Queue,
            session,
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


