from fastapi import APIRouter

from api.v1.routers.queues_entries import router as queues_entries_views_router
from api.v1.routers.tags import router as tags_router
from .auth.auth_routers import router as auth_router
from .queue_tag import router as queue_tag_router
from .queues import router as queues_views_router

router = APIRouter(
    prefix="/api_v1",
)

router.include_router(auth_router)
router.include_router(queues_views_router)
router.include_router(queues_entries_views_router)
router.include_router(tags_router)
router.include_router(queue_tag_router)

