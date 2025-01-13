from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from core.models import db_helper
from repositories.user import UserRepository
from schemas.user_schemas import UserUpdate, ManageUserPermissions
from services.user import UserService

async def get_user_service(
        session:"AsyncSession" = Depends(db_helper.session_getter)
) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

router = APIRouter(
    prefix="/manage",
    tags=[""],
)

@router.put(
    "",
    response_model=ManageUserPermissions,
    status_code=status.HTTP_200_OK,
)
async def manage_users(
        service: Annotated[UserService,Depends(get_user_service)],
        user_to_mange: ManageUserPermissions,
):
    return await service.update(user_to_mange.email,user_to_mange.model_dump(exclude_none=True))