from fastapi import APIRouter

from core.config import settings

from .auth import router as auth_router
from .health import router as health_router
from .queue_tag import router as queue_tag_router
from .queues import router as queues_views_router
from .queues_entries import router as queues_entries_views_router
from .tags import router as tags_router
from .user_manager import router as custom_router

router = APIRouter(prefix=settings.api_v1.prefix)


router.include_router(custom_router)
router.include_router(auth_router)
router.include_router(queues_views_router)
router.include_router(queues_entries_views_router)
router.include_router(tags_router)
router.include_router(queue_tag_router)
router.include_router(health_router)

__all__ = ["router"]
