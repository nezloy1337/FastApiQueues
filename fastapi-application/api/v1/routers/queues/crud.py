from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from schemas.queue_schemas import CreateQueue
from core.models.queue import Queue, QueueEntries
from utils.exception_handlers import average_handle_exception
from utils.logger import log_queue


async def create_queue(
    session: AsyncSession,
    queue_to_create: CreateQueue,
) -> Queue:
    try:
        # создаем модель и делаем запрос в базу данных
        queue = Queue(**queue_to_create.model_dump())
        session.add(queue)
        await session.commit()

        await log_queue(
            name=queue_to_create.name,
            start_time=datetime.combine(
                queue_to_create.start_time, datetime.min.time()
            ),
            max_slots=queue_to_create.max_slots,
            action="create",
            timestamp=datetime.now(),
        )

        return queue

    # обработка ошибки
    except Exception as e:
        if not isinstance(e, HTTPException):
            average_handle_exception(e)


async def get_queues(session: AsyncSession):
    try:
        # создаем запрос и делаем запрос в базу данных
        query = (
            select(Queue)
            .options(
                selectinload(Queue.queue_tags),
            )

        )

        result = await session.execute(query)
        return result.scalars().all()

    # обработка ошибки
    except Exception as e:
        average_handle_exception(e)


async def get_queue_with_entries(session: AsyncSession, queue_id: int):
    try:
        # создание запроса
        query = (
            select(Queue)
            .where(Queue.id == queue_id)
            .options(
                selectinload(Queue.entries).selectinload(QueueEntries.user),
                selectinload(Queue.queue_tags),  # Загружаем связанные теги
            )
        )

        # выполнения запроса
        result = await session.execute(query)
        return result.scalars().first()

    # обработка ошибок
    except Exception as e:
        average_handle_exception(e)
