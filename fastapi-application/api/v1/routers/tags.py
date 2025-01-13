from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies.tags import get_tags_service
from api.v1.routers.auth.fastapi_users_routers import current_user
from api.v1.routers.tags2 import crud
from core.models import User, db_helper
from schemas.tags import CreateTag, CreateTagQueue, GetTag, PatchTag
from services.tags import TagsService

router = APIRouter(
    tags=["tags"],
    prefix="/tags",
)


@router.post(
    "",
    response_model=CreateTag,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    tag_to_create: CreateTag,
    #user: Annotated[User, Depends(current_user)],
    service: Annotated[TagsService, Depends(get_tags_service)]
):
    return await service.create(tag_to_create.model_dump())


@router.post(
    "/tags/queue",
    response_model=CreateTagQueue,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag_queue(
    tag_queue_to_create: CreateTagQueue,
    user: Annotated[User, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.create_tag_queue(tag_queue_to_create, user, session)


@router.get(
    "/tags",
    response_model=List[GetTag],
    status_code=status.HTTP_200_OK,
)
async def get_tags(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    # user: Annotated[User, Depends(current_user)],
):
    return await crud.get_tags(session)


@router.delete(
    "tags2/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag(
    tag_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    # user: Annotated[User, Depends(current_user)],
):
    return await crud.delete_tag(tag_id, session)


@router.patch(
    "tags2/{tag_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatchTag,
)
async def patch_tag(
    tag_id: int,
    tag_patch: PatchTag,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    # user: Annotated[User, Depends(current_user)],
):
    return await crud.patch_tag(tag_id, tag_patch, session)
