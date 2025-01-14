
from repositories.queue_entry import QueueEntriesRepositoryExtended
from services.base import ExtendedBaseService


class QueueEntryServiceExtended(ExtendedBaseService):
    def __init__(self, repository: QueueEntriesRepositoryExtended):
        super().__init__(repository)
