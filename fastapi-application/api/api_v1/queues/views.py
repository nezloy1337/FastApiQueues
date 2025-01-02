from typing import Annotated, List
from fastapi import APIRouter
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from api.api_v1.queues.schemas import CreateQueue, Queue, GetQueue, GetQueueWithEntries
from core.models import db_helper
from . import crud

router = APIRouter(
    prefix="",
    tags=["queues"],
)


@router.post(
    "/queues",
    response_model=CreateQueue,
    status_code=status.HTTP_201_CREATED,
)
async def create_queue(
    queue_to_create: CreateQueue,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.create_queue(session, queue_to_create)


@router.get(
    "/queues",
    response_model=List[GetQueue],
    status_code=status.HTTP_200_OK,
)
async def get_queues(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.get_queues(session)


@router.get(
    "/queues/{queue_id}",
    response_model=GetQueueWithEntries,
    status_code=status.HTTP_200_OK,
)
async def get_queue_with_entries(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    queue_id: int,
):
    return await crud.get_queue_with_entries(session, queue_id)



