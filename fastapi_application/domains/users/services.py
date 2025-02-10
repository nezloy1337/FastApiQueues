from core.base.services import BaseService
from domains.users import User, UserRepository


class UserService(BaseService[User, UserRepository]):
    """
    Service layer for handling business logic related to users.

    Attributes:
        repository (UserRepository): The repository handling user operations.
    """

    pass
