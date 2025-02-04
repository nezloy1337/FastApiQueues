from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dependencies import (
    current_super_user,
    current_user,
    get_queue_entries_service,
)
from domains.queues import CreateQueueEntry, QueueEntryService
from domains.users import User

router = APIRouter(
    prefix="/queue",
    tags=["queues_entries"],
)


@router.post(
    "",
    response_model=CreateQueueEntry,
    status_code=status.HTTP_201_CREATED,
)
async def create_queue_entry(
    queue_entry_to_create: CreateQueueEntry,
    service: Annotated[QueueEntryService, Depends(get_queue_entries_service)],
    user: Annotated[User, Depends(current_user)],
):
    return await service.create(
        {
            **queue_entry_to_create.model_dump(),
            "user_id": user.id,
        }
    )


@router.delete(
    "/{queue_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_queue_entry(
    service: Annotated[QueueEntryService, Depends(get_queue_entries_service)],
    user: Annotated[User, Depends(current_user)],
    queue_id: int,
):
    return await service.delete({"queue_id": queue_id, "user_id": user.id})


@router.delete(
    "/{queue_id}/all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_queue_entry(
    service: Annotated[QueueEntryService, Depends(get_queue_entries_service)],
    user: Annotated[User, Depends(current_super_user)],
    queue_id: int,
):
    return await service.delete({"queue_id": queue_id})
