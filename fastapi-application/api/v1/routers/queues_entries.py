from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.v1.dependencies.queue_entry import get_queue_entries_service
from api.v1.routers.auth.fastapi_users_routers import current_user, current_super_user
from core.models import User
from schemas.queue_entries import CreateQueueEntry
from services.queue_entry import QueueEntryServiceExtended
from utils.api_v1 import combine_dict_with_user_uuid

router = APIRouter(
    prefix="/queue",
    tags=["queues_entries"],
)



@router.post(
    "/{queue_id}",
    response_model=CreateQueueEntry,
    status_code=status.HTTP_201_CREATED,
)
async def create_queue_entry(
    queue_entry_to_create: CreateQueueEntry,
    service: Annotated[QueueEntryServiceExtended, Depends(get_queue_entries_service)],
    user: Annotated[User, Depends(current_user)],
):
    return await service.create(
        combine_dict_with_user_uuid(
            queue_entry_to_create.model_dump(),
            user.id,
        )
    )


@router.delete(
    "/{queue_id}",
)
async def delete_queue_entry(
    service: Annotated[QueueEntryServiceExtended, Depends(get_queue_entries_service)],
    user: Annotated[User, Depends(current_user)],
    queue_id: int,
):
    return await service.delete(queue_id=queue_id,user_id=user.id)


@router.delete(
    "/{queue_id}/all",
)
async def clear_queue_entry(
        service: Annotated[QueueEntryServiceExtended, Depends(get_queue_entries_service)],
        user: Annotated[User, Depends(current_super_user)],
        queue_id: int,
):
    return await service.delete(queue_id=queue_id)