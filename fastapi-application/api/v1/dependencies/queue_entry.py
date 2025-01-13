from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.queue_entry import QueueEntriesRepository
from services.queue_entry import QueueEntryService


def get_queue_entries_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    repository = QueueEntriesRepository(session)
    return QueueEntryService(repository)