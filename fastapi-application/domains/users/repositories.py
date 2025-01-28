from sqlalchemy.ext.asyncio import AsyncSession

from core.base.repository import BaseRepository
from domains.users import User


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession, condition_builder):
        super().__init__(User, session, condition_builder)
