from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies.queue_entry import get_queue_entries_service
from api.v1.routers.auth.fastapi_users_routers import current_user
from api.v1.routers.queues_ent2ies import crud
from core.models import db_helper, User
from schemas.queue_entries import CreateQueueEntry
from services.queue_entry import QueueEntryService
from utils.api_v1 import combine_dict_with_user_uuid

router = APIRouter(
    prefix="/queue",
    tags=["queues_entries"],
)


# todo fix user_id problem
@router.post(
    "/{queue_id}",
    response_model=CreateQueueEntry,
    status_code=status.HTTP_201_CREATED,
)
async def create_queue_entry(
    queue_entry_to_create: CreateQueueEntry,
    service: Annotated[QueueEntryService, Depends(get_queue_entries_service)],
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
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_user)],
    queue_id: int,
):
    return await crud.delete_queues_entry(
        session,
        user,
        queue_id,
    )


@router.delete(
    "/queue/clear/{secret_code}",
)
async def clear_queue_entry(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    secret_code: str,
):
    # заглушка чтобы любой абобус не мог удалить
    if secret_code == "admin132":
        return await crud.clear_queues_entry(session)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="обойдешься"
        )
