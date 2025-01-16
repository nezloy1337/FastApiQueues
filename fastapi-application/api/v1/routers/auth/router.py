from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.v1.dependencies.services import get_user_service
from schemas.users import ManageUserPermissions
from services.user import UserService

router = APIRouter(
    prefix="/manage",
    tags=["custom"],
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
        user_to_mange.email, user_to_mange.model_dump(exclude_none=True)
    )
