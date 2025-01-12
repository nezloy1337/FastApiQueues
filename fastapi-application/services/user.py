from typing import Optional

from core.models import User
from repositories.user import UserRepository

from services.base import BaseService, T


class UserService(BaseService[User]):

    def __init__(self,repository: UserRepository):
        super().__init__(repository)

    async def update(self, obj_id: str, obj_data: dict) -> Optional[T]:
        return await self.repository.update(obj_id, obj_data)





