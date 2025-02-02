from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies import get_user_service
from domains.users import ManageUserPermissions, UserService

router = APIRouter(
    prefix="/manage",
    tags=["manage_users"],
)


@router.put(
    "",
    response_model=ManageUserPermissions,
    status_code=status.HTTP_200_OK,
)
async def manage_users(
    service: Annotated[UserService, Depends(get_user_service)],
    user_to_mange: ManageUserPermissions,
):
    return await service.patch(
        {"email": user_to_mange.email}, **user_to_mange.model_dump(exclude_none=True)
    )
