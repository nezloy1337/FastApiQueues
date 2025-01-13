from repositories.queue_entry import QueueEntriesRepository
from services.base import BaseService


class QueueEntryService(BaseService):
    def __init__(self,repository: QueueEntriesRepository):
        super().__init__(repository)