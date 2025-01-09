from typing import Annotated

from fastapi import APIRouter, status, Depends
from pygments.lexers import q
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.fastapi_users_routers import current_user
from api.api_v1.tags import crud
from api.api_v1.tags.schemas import CreateTag, CreateTagQueue
from core.models import User, db_helper

router = APIRouter(
    tags=["tags"],
    prefix="",
)


@router.post(
    "/tags",
    response_model=CreateTag,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    tag_to_create: CreateTag,
    user: Annotated[User, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.create_tag(tag_to_create, user, session)


@router.post(
    "tags/queue",
    response_model=CreateTagQueue,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag_queue(
    tag_queue_to_create: CreateTagQueue,
    user: Annotated[User, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.create_tag_queue(tag_queue_to_create, user, session)
