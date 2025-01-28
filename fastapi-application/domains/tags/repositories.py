from sqlalchemy.ext.asyncio import AsyncSession

from core.base.repository import BaseRepository
from domains.tags import Tags
from utils.condition_builder import ConditionBuilder


class TagsRepository(BaseRepository[Tags]):

    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            Tags,
            session,
            condition_builder,
        )
