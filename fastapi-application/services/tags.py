from core.models import User
from repositories.tags import TagsRepository
from services.base import BaseService


class TagsService(BaseService[User]):

    def __init__(self, repository: TagsRepository):
        super().__init__(repository)

