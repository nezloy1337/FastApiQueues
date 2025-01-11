from fastapi import APIRouter

from .auth.auth_routers import router as auth_router
from .queues_router import router as queues_views_router
from api.v1.routers.queues_entries_router import router as queues_entries_views_router
from api.v1.routers.tags_router import router as tags_router

router = APIRouter(
    prefix="/api_v1",
)

router.include_router(auth_router)
router.include_router(queues_views_router)
router.include_router(queues_entries_views_router)
router.include_router(tags_router)

