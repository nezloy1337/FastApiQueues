from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies.queues import get_queue_service
from schemas.queue_schemas import CreateQueue, GetQueue, GetQueueWithEntries
from core.models import db_helper, User
from api.v1.routers.queues import crud
from api.v1.routers.auth.fastapi_users_routers import current_user
from services.queue import QueueService

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
    service: Annotated[QueueService, Depends(get_queue_service)],
):
    return await service.create(queue_to_create.model_dump())

######
@router.get(
    "/queues",
    response_model=List[GetQueue],
    status_code=status.HTTP_200_OK,
)
async def get_queues(
    service:Annotated[QueueService,Depends(get_queue_service)],
    #user: Annotated[User, Depends(current_user)],
):
    return await service.get_all()


@router.get(
    "/queues/{queue_id}",
    response_model=GetQueueWithEntries | None,
    status_code=status.HTTP_200_OK,
)
async def get_queue_with_entries(
    queue_id: int,
    #user: Annotated[User, Depends(current_user)],
    service: Annotated[QueueService,Depends(get_queue_service)],
):
    return await service.get_by_id(queue_id)
