from core.models import QueueTags
from repositories.queue_tags import QueueTagsRepository
from services.base import BaseService


class QueueTagService(BaseService[QueueTags]):
    def __init__(self,repository: QueueTagsRepository):
        super().__init__(repository)
