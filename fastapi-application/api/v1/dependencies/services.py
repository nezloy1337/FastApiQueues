from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repositories.queue import QueueRepository
from repositories.queue_entry import QueueEntriesRepository
from repositories.queue_tags import QueueTagsRepository
from repositories.tags import TagsRepository
from repositories.user import UserRepository
from services.queue import QueueService
from services.queue_entry import QueueEntryServiceExtended
from services.queue_tag import QueueTagService
from services.tags import TagsService
from services.user import UserService


async def get_user_service(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


def get_queue_entries_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    repository = QueueEntriesRepository(session)
    return QueueEntryServiceExtended(repository)


async def get_tags_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    tags_repository = TagsRepository(session)
    return TagsService(tags_repository)


async def get_queue_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> QueueService:
    queue_repository = QueueRepository(session)
    return QueueService(queue_repository)


def get_queue_tags_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    repository = QueueTagsRepository(session)
    return QueueTagService(repository)
