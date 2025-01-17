from typing import Type, Callable, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from repositories import TRepositories
from services import TService
from utils.exception_handlers import get_exception_handler, ExceptionHandler


# нужен ли async


class ServiceFactory:
    @staticmethod
    def create(
        service_cls: Type[TService],
        repository_cls: Type[TRepositories],


    ) -> Callable[[AsyncSession], TService]:
        """
        Создаёт фабрику для сервиса с указанным репозиторием.
        :param exception_handler:
        :param service_cls: Класс сервиса.
        :param repository_cls: Класс репозитория.
        :return: Callable, создающий сервис.
        """

        def _get_service(
            session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
            exception_handler = Annotated[ExceptionHandler, Depends(get_exception_handler)],
        ) -> TService:
            repository = repository_cls(session)
            return service_cls(repository,exception_handler)

        return _get_service
