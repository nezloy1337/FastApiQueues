from repositories.queue_tags import QueueTagsRepository
from services.base import BaseService


class QueueTagService(BaseService):
    def __init__(self,repository: QueueTagsRepository):
        super().__init__(repository)
