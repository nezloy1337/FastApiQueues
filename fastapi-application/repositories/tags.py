from sqlalchemy.ext.asyncio import AsyncSession

from models import Tags
from repositories import BaseRepository


class TagsRepository(BaseRepository[Tags]):

    def __init__(self, session: AsyncSession):
        super().__init__(
            Tags,
            session,
        )
