from sqlalchemy.ext.asyncio import AsyncSession

from core.base.repository import BaseRepository
from domains.tags import Tags
from utils.condition_builder import ConditionBuilder


class TagsRepository(BaseRepository[Tags]):
    """
    Repository for managing Tags-related database operations.

    Attributes:
        session (AsyncSession): The database session.
        condition_builder (ConditionBuilder): Utility for building query conditions.
    """

    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            Tags,
            session,
            condition_builder,
        )
