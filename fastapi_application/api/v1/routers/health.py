from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(
    tags=["health"],
    prefix="/health",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_tag_queue():
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200,
    )
