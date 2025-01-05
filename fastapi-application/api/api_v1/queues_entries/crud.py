from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from api.api_v1.queues_entries.schemas import CreateQueueEntryWithAuth
from core.config import settings
from core.models import QueueEntries, User


import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def create_queues_entry(
    session: AsyncSession,
    queue_entry_to_create: CreateQueueEntryWithAuth,
    user: User,
) -> QueueEntries:
    try:
        # создание записи в бд
        queue_entry = QueueEntries(
            **queue_entry_to_create.model_dump(), user_id=str(user.id)
        )
        session.add(queue_entry)
        await session.commit()
        return queue_entry

    except IntegrityError as e:
        # Логирование ошибки
        logger.error(f"Ошибка при добавлении записи в очередь: {e.args}")

        # Откат транзакции
        await session.rollback()

        # Возврат HTTPException
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже зарегистрирован в данной очереди.",
        )


async def clear_queues_entry(
    session: AsyncSession,
):
    try:
        result = await session.execute(select(QueueEntries))
        to_delete = result.scalars().all()
        for record in to_delete:
            await session.delete(record)
        await session.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
