from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from fastapi import HTTPException, status

from core.base import TModels
from core.base.repository import AbstractRepository
from utils.exception_handlers import handle_exception


class AbstractService(ABC, Generic[TModels]):
    """
    Абстрактный базовый класс для всех сервисов.
    """

    @abstractmethod
    async def create(self, obj_data: dict) -> TModels:
        """
        Создает новый объект.
        :param obj_data: данные для создания объекта.
        :return: созданный объект.
        """
        pass

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        """
        Получает объект по идентификатору.
        :param obj_id: идентификатор объекта.
        :return: объект или None, если не найден.
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[TModels]:
        """
        Получает список всех объектов.
        :return: список объектов.
        """
        pass

    @abstractmethod
    async def delete(self, **conditions) -> bool:
        """
        Удаляет объект, соответствующий условиям.
        :param conditions: условия удаления.
        :return: True, если удаление успешно.
        """
        pass

    @abstractmethod
    async def patch(self, filters: dict, **values) -> dict:
        """
        Обновляет объект(ы) по фильтрам.
        :param filters: фильтры для поиска объектов.
        :param values: значения для обновления.
        :return: обновленные данные.
        """
        pass


class BaseService(AbstractService,Generic[TModels]):
    def __init__(
        self,
        repository: AbstractRepository[TModels],
    ):
        self.repository = repository

    @handle_exception
    async def create(self, obj_data: dict) -> TModels:
        return await self.repository.create(obj_data)

    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> List[TModels]:
        return await self.repository.get_all()

    async def delete(self, **conditions) -> bool:
        if await self.repository.delete(**conditions):
            return True
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")

    async def patch(self, filters, **values) -> dict:
        try:
            if data := await self.repository.patch({**filters}, **values):
                return data
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found"
            )
        except Exception as e:
            raise


TService = TypeVar(
    "TService",
    bound=AbstractService,
)
