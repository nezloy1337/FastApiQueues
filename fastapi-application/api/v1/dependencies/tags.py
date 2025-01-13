from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from core.models import db_helper
from repositories.tags import TagsRepository
from services.tags import TagsService


async def get_tags_service(
        session: Annotated[AsyncSession,Depends(db_helper.session_getter)],
):
    tags_repository = TagsRepository(session)
    return TagsService(tags_repository)