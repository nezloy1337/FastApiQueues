from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.queue import QueueRepository
from services.queue import QueueService


async def get_queue_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> QueueService:
    queue_repository = QueueRepository(session)
    return QueueService(queue_repository)
