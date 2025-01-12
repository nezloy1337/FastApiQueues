from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Queue
from repositories.base import BaseRepository


class QueueRepository(BaseRepository[Queue]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            Queue,
            session,
        )
