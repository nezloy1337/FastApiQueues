from fastapi import APIRouter
from .auth import router as auth_router
from .views import router as views_router

router = APIRouter(
    prefix="/api_v1",
)

router.include_router(auth_router)
router.include_router(views_router)

