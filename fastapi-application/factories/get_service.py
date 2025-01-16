from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from repositories.base import TRepository
from services.base import TService


# нужен ли async


class ServiceFactory:
    @staticmethod
    def create(
        service_cls: Type[TService],
        repository_cls: Type[TRepository],
    ) -> Callable[[AsyncSession], TService]:
        """
        Создаёт фабрику для сервиса с указанным репозиторием.
        :param service_cls: Класс сервиса.
        :param repository_cls: Класс репозитория.
        :return: Callable, создающий сервис.
        """

        def _get_service(
            session: AsyncSession = Depends(db_helper.session_getter),
        ) -> TService:
            repository = repository_cls(session)
            return service_cls(repository)

        return _get_service
