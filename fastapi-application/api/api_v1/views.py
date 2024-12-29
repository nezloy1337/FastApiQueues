from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends,Request


from api.api_v1.fastapi_users_routers import current_user
from core.models import User
from core.schemas.user import UserRead

router = APIRouter(
    prefix="/api/test",
    tags=["test"],
)


@router.get("/")
def get_something(
    user: Annotated[User,Depends(current_user)],
    request: Request,
):
    print(request)
    return {"message": "Hello World",
            "user": UserRead.model_validate(user)}
