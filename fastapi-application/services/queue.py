from repositories.queue import QueueRepository
from services.base import BaseService


class QueueService(BaseService):
    def __init__(self,repository: QueueRepository):
        super().__init__(repository)