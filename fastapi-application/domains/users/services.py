from core.base.services import BaseService
from domains.users import User, UserRepository


class UserService(BaseService[User, UserRepository]):
    pass
