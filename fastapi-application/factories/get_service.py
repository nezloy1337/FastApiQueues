from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from factories.condition_builder import ConditionBuilderFactory, get_condition_builder_factory
from repositories import TRepositories, BaseRepository
from services import TService


def get_repository(
    repository_type: Type[TRepositories],
) -> Callable[[AsyncSession], BaseRepository]:
    def create_repository(
        session: AsyncSession = Depends(db_helper.session_getter),
        builder_factory: ConditionBuilderFactory = Depends(get_condition_builder_factory),
    ) -> Type[TRepositories]:
        return repository_type(session, builder_factory,)

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

