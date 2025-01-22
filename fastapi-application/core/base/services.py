from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypeVar

from fastapi import HTTPException, status

from core.base import TModels
from core.base.repository import AbstractRepository
from utils.exception_handlers import handle_exception


class AbstractService(ABC):
    """
    Абстрактный базовый класс для всех сервисов.

    :param TModels: Тип модели, с которой работает сервис.
    """

    @abstractmethod
    async def create(self, obj_data: dict) -> TModels:
        """
        Создаёт новый объект.

        :param obj_data: Данные для создания объекта.
        :return: Созданный объект модели.
        """
        pass

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        """
        Получает объект по идентификатору.

        :param obj_id: Идентификатор объекта.
        :return: Объект модели или None, если не найден.
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[TModels]:
        """
        Получает список всех объектов.

        :return: Список объектов модели.
        """
        pass

    @abstractmethod
    async def delete(self, **conditions) -> bool:
        """
        Удаляет объект, соответствующий условиям.

        :param conditions: Условия удаления (например, id=1, name='test').
        :return: True, если хотя бы один объект был удалён.
        """
        pass

    @abstractmethod
    async def patch(self, filters: Dict[str, Any], **values: Any) -> Dict[str, Any]:
        """
        Обновляет объект(ы) по фильтрам.

        :param filters: Фильтры для поиска объектов (например, {"id": 1}).
        :param values: Значения для обновления (например, name="New Name").
        :return: Словарь с обновлёнными данными.
        """
        pass


class BaseService(AbstractService):
    """
    Базовый сервис, реализующий логику работы с абстрактным репозиторием.

    :param repository: Экземпляр репозитория, реализующего операции над моделью.
    """

    def __init__(
        self,
        repository: "AbstractRepository[TModels]",
    ):
        self.repository = repository

    @handle_exception
    async def create(self, obj_data: dict) -> TModels:
        """
        Создаёт новый объект в базе данных.

        :param obj_data: Данные для создания объекта.
        :return: Созданный объект модели.
        """
        return await self.repository.create(obj_data)

    @handle_exception
    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        """
        Возвращает объект по идентификатору.

        :param obj_id: Идентификатор объекта.
        :return: Объект модели или None, если не найден.
        """
        obj = await self.repository.get_by_id(obj_id)

        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )
        return obj

    @handle_exception
    async def get_all(self) -> List[TModels]:
        """
        Возвращает список всех объектов.

        :return: Список объектов модели.
        """
        return await self.repository.get_all()

    @handle_exception
    async def delete(self,filters: dict[str, Any]) -> bool:
        """
        Удаляет объект, соответствующий условиям.

        :param filters: Фильтры поиска объектов (например, {"id": 1}).
        :return: True, если объект успешно удалён.
        :raises HTTPException: Если объект не найден.
        """
        deleted_obj = await self.repository.delete(**filters)
        if deleted_obj:
            return True

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not Found",
        )

    @handle_exception
    async def patch(
        self,
        filters: dict[str, Any],
        **values: Any,
    ) -> dict[str, Any] | None:
        """
        Обновляет объект(ы) по заданным фильтрам и возвращает обновлённые данные.

        :param filters: Фильтры поиска объектов (например, {"id": 1}).
        :param values: Значения для обновления (например, name="New Name").
        :return: Словарь обновлённых данных.
        :raises HTTPException: Если объект не найден.
        """
        patched_obj = await self.repository.patch(filters, **values)
        if patched_obj:
            return patched_obj

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )


TService = TypeVar(
    "TService",
    bound=AbstractService,
)
