from typing import Annotated
from fastapi import APIRouter, HTTPException
from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from api.api_v1.auth.fastapi_users_routers import current_user
from api.api_v1.queues_entries.crud import create_queues_entry, clear_queues_entry, delete_queues_entry
from api.api_v1.queues_entries.schemas import CreateQueueEntry, QueueEntry, CreateQueueEntryWithAuth
from core.models import db_helper, User

from core.models import QueueEntries


router = APIRouter(
    prefix="",
    tags=["queues_entries"],
)


@router.post(
    "/queues/{queue_id}/take",
    response_model=CreateQueueEntryWithAuth,
    status_code=status.HTTP_200_OK,
)
async def create_queue_entry(
    queue_entry_to_create: CreateQueueEntryWithAuth,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_user)],


):
    return await create_queues_entry(session, queue_entry_to_create, user)


@router.get(
    "/queue/{queue_id}",
    response_model=QueueEntry,
)
async def get_queue_entry(
    queue_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    pass


@router.delete(
    "/queue/{queue_id}/delete",
)
async def delete_queue_entry(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: Annotated[User, Depends(current_user)],
        queue_id: int
):
    return await delete_queues_entry(session, user,queue_id)


@router.delete(
    "/queue/clear/{secret_code}",
)
async def clear_queue_entry(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    secret_code: str
):
    #заглушка чтобы любой абобус не мог удалить
    if secret_code == "admin132":
        return await clear_queues_entry(session)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="обойдешься")
