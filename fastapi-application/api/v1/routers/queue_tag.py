from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.v1.dependencies.queue_tags import get_queue_tags_service
from schemas.tags import CreateTagQueue
from services.tags import TagsService

router = APIRouter(
    tags=["queue_tag"],
    prefix="/queue_tag",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def create_tag_queue(
    # user: Annotated[User, Depends(current_user)],
    service: Annotated[TagsService, Depends(get_queue_tags_service)]
):
    return await service.get_all()


@router.post(
    "",
    response_model=CreateTagQueue,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag_queue(
    tag_queue_to_create: CreateTagQueue,
    # user: Annotated[User, Depends(current_user)],
    service: Annotated[TagsService, Depends(get_queue_tags_service)],
):
    return await service.create(tag_queue_to_create.model_dump())


@router.delete(
    "/{ tag_id }",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag_queue(
    tag_id: int,
    # user: Annotated[User, Depends(current_user)],
    service: Annotated[TagsService, Depends(get_queue_tags_service)],
):
    return await service.delete(id=tag_id)
