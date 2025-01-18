from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from repositories import TRepositories, BaseRepository
from services import TService
from utils.condition_builder import ConditionBuilder, get_condition_builder


def get_repository(
    repository_type: Type[TRepositories],
) -> Callable[[AsyncSession], BaseRepository]:
    def create_repository(
        session: AsyncSession = Depends(db_helper.session_getter),
        condition_builder: ConditionBuilder = Depends(get_condition_builder(repository_type)),
    ) -> Type[TRepositories]:
        return repository_type(session, condition_builder,)

    return create_repository



def get_service(
    service_cls: Type[TService],
    repository_cls: Type[TRepositories],
) -> Callable[[], TService]:
    def create_service(
        repository: TRepositories = Depends(get_repository(repository_cls)),
    ) -> TService:
        return service_cls(repository)

    return create_service

