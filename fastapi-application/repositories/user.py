from fastapi import HTTPException,status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from repositories.base import BaseRepository
from schemas.user_schemas import UserUpdate


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(
            User,
            session,
        )

    async def update(self, email: str, obj_data: dict) -> dict:
        query = update(self.model).where(self.model.email == email).values(**obj_data)
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update failed:now data is changed",
            )
        await self.session.commit()
        return obj_data

