
from repositories.queue_entry import QueueEntriesRepository
from services.base import BaseServiceWithExtraParams


class QueueEntryService(BaseServiceWithExtraParams):
    def __init__(self,repository: QueueEntriesRepository):
        super().__init__(repository)
