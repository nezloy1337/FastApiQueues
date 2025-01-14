from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueEntries
from repositories.base import BaseRepositoryWithExtraParams


class QueueEntriesRepository(BaseRepositoryWithExtraParams[QueueEntries]):
    def __init__(self,session: AsyncSession):
        super().__init__(QueueEntries,session,)


