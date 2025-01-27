from typing import (
    Any,
    Generic,
    Type,
)

from sqlalchemy import and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.condition_builder import ConditionBuilder

from core.types import TModels


class BaseRepository(Generic[TModels]):
    """
    Base repository implementing common CRUD operations for SQLAlchemy models.

    :param model: The SQLAlchemy model class managed by the repository.
    :param session: The asynchronous SQLAlchemy session.
    :param condition_builder: An object that generates
     filter (WHERE) conditions from dictionaries.
    """

    def __init__(
        self,
        model: Type[TModels],
        session: AsyncSession,
        condition_builder: "ConditionBuilder",  # Кавычки для аннотации,
    ):  # если класс объявлен позже
        self.model = model
        self.session = session
        self.condition_builder = condition_builder

    async def create(self, obj_data: dict) -> TModels:
        """
        Creates a new object based on the provided data and saves it to the database.

        :param obj_data: A dictionary containing the data for the new record.
        :return: The created model instance.
        """
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, obj_id: int) -> TModels | None:
        """
        Retrieves an object by its unique identifier (ID).

        :param obj_id: The unique identifier of the record.
        :return: The model instance or None if not found.
        """
        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> list[TModels]:
        """
        Retrieves all objects of the model from the database.

        :return: A list of model instances.
        """
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, **conditions: dict) -> TModels | None:
        """
        Deletes an object matching the specified
        conditions and returns the deleted object.
        Returns None if no matching object is found.

        :param conditions: Arbitrary conditions for filtering objects.
        :return: The deleted object or None if no matching object is found.
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
        Updates an object based on the specified filters and returns the updated object.
        Returns None if no object is found.

        :param filters: A dictionary of filters for identifying the record
        (e.g., {"id": 1} or {"email": "EMAIL"}).
        :param values: Arbitrary key-value pairs for updating the record fields
        (e.g., name="New Name").
        :return: The updated object or None if no matching record is found.
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
