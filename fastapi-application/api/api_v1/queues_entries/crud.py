from fastapi import HTTPException, status, Response
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from api.api_v1.queues_entries.schemas import CreateQueueEntryWithAuth
from core.config import settings
from core.models import QueueEntries, User
from utils.exception_handlers import create_queue_entry_handle_exception, delete_queue_entry_handle_exception

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def create_queues_entry(
    session: AsyncSession,
    queue_entry_to_create: CreateQueueEntryWithAuth,
    user: User,
) -> QueueEntries:
    try:
        # создание запроса
        queue_entry = QueueEntries(
            **queue_entry_to_create.model_dump(),
            user_id=str(user.id),
        )

        # выполнение запроса
        session.add(queue_entry)
        await session.commit()
        return queue_entry

    # разбираемся с ошибкой
    except Exception as e:
        create_queue_entry_handle_exception(e)

#TODO правильный обработчик ошибок
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


async def delete_queues_entry(session: AsyncSession, user: User, queue_id):
    try:
        # запрашиваем запись с занятой очередью
        query = await session.execute(
            select(QueueEntries).where(
                and_(
                    QueueEntries.user_id == str(user.id),
                    QueueEntries.queue_id == queue_id,
                )
            )
        )

        # получаем объект занятой очереди
        if queue_to_delete := query.scalars().first():
            await session.delete(queue_to_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        # ошибка если нет такого объекта
        delete_queue_entry_handle_exception(
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=settings.errors_description.no_entry_description,
        ))

    # любые другие ошибки
    except Exception as e:
        delete_queue_entry_handle_exception(e)
