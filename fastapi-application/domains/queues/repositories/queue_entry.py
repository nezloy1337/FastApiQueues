from sqlalchemy.ext.asyncio import AsyncSession

from domains.queues import QueueEntries
from repositories import BaseRepository
from utils.condition_builder import ConditionBuilder


class QueueEntriesRepository(BaseRepository[QueueEntries]):
    def __init__(self,session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(QueueEntries,session,condition_builder)


