from core.models import User
from repositories.user import UserRepository
from services.base import BaseService


class UserService(BaseService[User]):

    def __init__(self,repository: UserRepository):
        super().__init__(repository)







