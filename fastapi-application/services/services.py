from repositories.queue import QueueRepository
from repositories.queue_entry import QueueEntriesRepository
from repositories.queue_tags import QueueTagsRepository
from repositories.tags import TagsRepository
from repositories.user import UserRepository
from services.base import BaseService


class QueueEntryService(BaseService):
    def __init__(self, repository: QueueEntriesRepository):
        super().__init__(repository)


class QueueTagService(BaseService):
    def __init__(self,repository: QueueTagsRepository):
        super().__init__(repository)


class TagsService(BaseService):

    def __init__(self, repository: TagsRepository):
        super().__init__(repository)


class UserService(BaseService):

    def __init__(self,repository: UserRepository):
        super().__init__(repository)


class QueueService(BaseService):
    def __init__(self,repository: QueueRepository):
        super().__init__(repository)