from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from api.v1.dependencies import get_queue_service, current_super_user
from domains.queues import QueueService
from domains.queues.schemas.queues import CreateQueue, GetQueue, GetQueueWithEntries, PutQueue
from domains.users import User
from utils.logger import log_action

router = APIRouter(
    prefix="/queues",
    tags=["queues"],
)


@router.get(
    "",
    response_model=List[GetQueue],
    status_code=status.HTTP_200_OK,
)
async def get_queues(
    service: Annotated[QueueService, Depends(get_queue_service)],
    # user: Annotated[User, Depends(current_user)],
):
    return await service.get_all()



@router.post(
    "",
    response_model=CreateQueue,
    status_code=status.HTTP_201_CREATED,
)
@log_action(
    action="POST",
    collection_name="queues",
    log_params=["queue_to_create","user"]
)
async def create_queue(
    queue_to_create: CreateQueue,
    service: Annotated[QueueService, Depends(get_queue_service)],
):
    return await service.create(queue_to_create.model_dump())

@router.get(
    "/{queue_id}",
    response_model=GetQueueWithEntries | None,
    status_code=status.HTTP_200_OK,
)
async def get_queue_with_entries(
    queue_id: int,
    # user: Annotated[User, Depends(current_user)],
    service: Annotated[QueueService, Depends(get_queue_service)],
):
    return await service.get_by_id(queue_id)


@router.put(
    "/{queue_id}",
    response_model=PutQueue,
)
@log_action(
    action="PUT",
    collection_name="queues",
    log_params=["queue_to_patch","user","queue_id"]
)
async def put_queue(
    queue_to_patch: PutQueue,
    queue_id: int,
    service: Annotated[QueueService, Depends(get_queue_service)],
    user: Annotated[User, Depends(current_super_user)],
):
    return await service.patch(queue_id, **queue_to_patch.model_dump(exclude_none=True))


@router.delete(
    "/{queue_id}",
    response_model=bool,
)
@log_action(
    action="POST",
    collection_name="queues",
    log_params=["queue_id","user"]
)
async def delete_queue(
    queue_id: int,
    service: Annotated[QueueService, Depends(get_queue_service)],
    user: Annotated[User, Depends(current_super_user)],
):
    return await service.delete(id = queue_id)
