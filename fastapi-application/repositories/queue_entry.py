from sqlalchemy.ext.asyncio import AsyncSession

from core.models import QueueEntries
from repositories.base import ExtendedBaseRepository


class QueueEntriesRepositoryExtended(ExtendedBaseRepository[QueueEntries]):
    def __init__(self,session: AsyncSession):
        super().__init__(QueueEntries,session,)


