from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.queue_entry import QueueEntriesRepositoryExtended
from services.queue_entry import QueueEntryServiceExtended


def get_queue_entries_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    repository = QueueEntriesRepositoryExtended(session)
    return QueueEntryServiceExtended(repository)