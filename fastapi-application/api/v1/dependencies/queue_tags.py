from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.queue_tags import QueueTagsRepository
from services.queue_tag import QueueTagService


def get_queue_tags_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    repository = QueueTagsRepository(session)
    return QueueTagService(repository)
