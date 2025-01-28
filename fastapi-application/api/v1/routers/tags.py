from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from api.dependencies import current_super_user, current_user, get_tags_service
from domains.tags import CreateTag, GetTag, PatchTag, TagsService
from domains.users import User

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
    user: Annotated[User, Depends(current_super_user)],
    service: Annotated[TagsService, Depends(get_tags_service)],
):
    return await service.create(tag_to_create.model_dump())


@router.get(
    "",
    response_model=List[GetTag],
    status_code=status.HTTP_200_OK,
)
async def get_tags(
    service: Annotated[TagsService, Depends(get_tags_service)],
    user: Annotated[User, Depends(current_user)],
):
    return await service.get_all()


@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag(
    tag_id: int,
    service: Annotated[TagsService, Depends(get_tags_service)],
    user: Annotated[User, Depends(current_super_user)],
):
    return await service.delete({"id": tag_id})


@router.patch(
    "/{tag_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatchTag,
)
async def patch_tag(
    tag_id: int,
    tag_patch: PatchTag,
    service: Annotated[TagsService, Depends(get_tags_service)],
    user: Annotated[User, Depends(current_super_user)],
):
    return await service.patch({"id": tag_id}, **tag_patch.model_dump())
