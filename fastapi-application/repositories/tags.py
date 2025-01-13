from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tags
from repositories.base import BaseRepository


class TagsRepository(BaseRepository[Tags]):

    def __init__(self, session: AsyncSession):
        super().__init__(
            Tags,
            session,
        )
