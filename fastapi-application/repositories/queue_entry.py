from sqlalchemy.ext.asyncio import AsyncSession

from models import QueueEntries
from repositories.base import BaseRepository


class QueueEntriesRepository(BaseRepository[QueueEntries]):
    def __init__(self,session: AsyncSession):
        super().__init__(QueueEntries,session,)


