from sqlalchemy.ext.asyncio import AsyncSession

from domains.queues import QueueTags
from repositories import BaseRepository
from utils.condition_builder import ConditionBuilder


class QueueTagsRepository(BaseRepository):
    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            QueueTags,
            session,
            condition_builder,
        )
