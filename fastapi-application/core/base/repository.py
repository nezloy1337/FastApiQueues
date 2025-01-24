from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar, Union,
)

from sqlalchemy import update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.base import TModels
from utils.condition_builder import ConditionBuilder


class AbstractRepository(ABC, Generic[TModels]):
    """
    Абстрактный класс репозитория, задающий интерфейс для работы с моделью SQLAlchemy.

    :param TModels: Тип SQLAlchemy-модели, с которой работает репозиторий.
    """

    @abstractmethod
    async def create(self, obj_data: dict) -> TModels:
        """
        Создаёт новую запись в базе данных на основе переданных данных.

        :param obj_data: Словарь с данными для создания записи.
        :return: Созданный экземпляр SQLAlchemy-модели.
        """
        pass

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        """
        Получает запись по её уникальному идентификатору (ID).

        :param obj_id: Идентификатор записи.
        :return: Найденный экземпляр модели или None, если запись не найдена.
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[TModels]:
        """
        Получает все записи из базы данных для указанной модели.

        :return: Список экземпляров модели.
        """
        pass

    @abstractmethod
    async def delete(self, **conditions: dict) -> bool:
        """
        Удаляет объекты, соответствующие указанным условиям.

        :param conditions: Произвольные условия для удаления (например, id=1, name="test").
        :return: True, если хотя бы одна запись была удалена, иначе False.
        """
        pass

    @abstractmethod
    async def patch(
        self,
        filters: Dict[str, Any],
        **values: Any,
    ) -> dict[str, Any] | None:
        """
        Обновляет объект с указанным уникальным ключом, возвращая словарь обновлённых
        полей или None, если запись не найдена.

        :param filters Словарь (уникальный ключ), по которому ищется запись
        (например, {"id": 1}).
        :param values: Произвольные ключи и значения для обновления полей.
        :return: Словарь обновлённых полей или None, если запись не найдена.
        """
        pass


class BaseRepository(AbstractRepository[TModels]):
    """
    Базовый репозиторий, реализующий основные CRUD-операции для SQLAlchemy-моделей.

    :param model: Класс SQLAlchemy-модели, с которой работает репозиторий.
    :param session: Асинхронная сессия SQLAlchemy.
    :param condition_builder: Объект, создающий условия для фильтрации (WHERE) на основе словаря.
    """

    def __init__(
        self,
        model: Type[TModels],
        session: AsyncSession,
        condition_builder: "ConditionBuilder",  # Кавычки для аннотации, если класс объявлен позже
    ):
        self.model = model
        self.session = session
        self.condition_builder = condition_builder

    async def create(self, obj_data: dict) -> TModels:
        """
        Создаёт новый объект на основе переданных данных и сохраняет его в базе данных.

        :param obj_data: Словарь с данными для создания записи.
        :return: Созданный экземпляр модели.
        """
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, obj_id: int) -> TModels | None:
        """
        Ищет объект по его уникальному идентификатору (ID).

        :param obj_id: Идентификатор записи.
        :return: Объект модели или None, если запись не найдена.
        """
        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> List[TModels]:
        """
        Возвращает список всех объектов модели из базы данных.

        :return: Список экземпляров модели.
        """
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, **conditions: dict) -> TModels | None:
        """
        Удаляет объект, соответствующий указанным условиям, и удалённый объект.
        Если объект не найдены, возвращается None.

        :param conditions: Произвольные условия для фильтрации объектов.
        :return: Удалённый объект или None, если ничего не удалено.
        """
        query_conditions = self.condition_builder.create_conditions(**conditions)

        stmt = delete(self.model).filter(and_(*query_conditions)).returning(self.model)

        result = await self.session.execute(stmt)
        deleted_obj = result.scalar_one_or_none()
        if deleted_obj:
            await self.session.commit()
        return deleted_obj

    async def patch(
        self,
        filters: dict[str, Any],
        **values: Any,
    ) -> TModels | None:
        """
        Обновляет объект на основе словаря фильтров, и возвращает обновлённый объект
        Если объекты не найдены, возвращается None.

        :param filters: Словарь фильтров для поиска записи
        (например, {"id": 1,} или {"email":"EMAIL"}).
        :param values: Произвольные ключи и значения для обновления полей
        (например, name="New Name").
        :return: Обновлённый объект или None, если ничего не обновлено.
        """
        # Формируем условия для фильтрации
        conditions = self.condition_builder.create_conditions(**filters)
        if not conditions:
            return None

        stmt = (
            update(self.model)
            .filter(*conditions)
            .values(**values)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)
        updated_obj = result.scalar_one_or_none()

        if updated_obj:
            await self.session.commit()
        return updated_obj


TRepositories = TypeVar(
    "TRepositories",
    bound=Union["QueueRepository"],
)
