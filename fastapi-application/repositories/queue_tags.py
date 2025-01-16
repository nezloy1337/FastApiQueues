from sqlalchemy.ext.asyncio import AsyncSession

from models import QueueTags
from repositories.base import BaseRepository


class QueueTagsRepository(BaseRepository):
    def __init__(self,session: AsyncSession):
        super().__init__(QueueTags,session,)
