from typing import Any, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import and_, delete, update

from core.types import TModels
from utils.condition_builder import ConditionBuilder


class BaseRepository(Generic[TModels]):
    """
    A base repository that provides common CRUD operations for SQLAlchemy models.

    This repository handles asynchronous database operations using SQLAlchemy and
    provides a standardized way to interact with models.

    Attributes:
        model (Type[TModels]): The SQLAlchemy model managed by this repository.
        session (AsyncSession): The asynchronous SQLAlchemy session.
        condition_builder (ConditionBuilder):
        A utility for generating filtering conditions.
    """

    def __init__(
        self,
        model: Type[TModels],
        session: AsyncSession,
        condition_builder: "ConditionBuilder",  # Quotes for forward declaration
    ):
        """
        Initializes the repository with a model,
        database session, and condition builder.

        Args:
            model (Type[TModels]): The SQLAlchemy model associated with this repository.
            session (AsyncSession): The asynchronous database session.
            condition_builder (ConditionBuilder):
            A condition builder for dynamic filtering.
        """

        self.model = model
        self.session = session
        self.condition_builder = condition_builder

    async def create(self, obj_data: dict[str, Any]) -> TModels:
        """
        Creates and persists a new record in the database.

        Args:
            obj_data (dict[str, Any]):
            A dictionary containing field values for the new object.

        Returns:
            TModels: The created model instance.
        """

        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, obj_id: int) -> TModels | None:
        """
        Retrieves a record by its unique identifier (ID).

        Args:
            obj_id (int): The unique identifier of the record.

        Returns:
            TModels | None: The retrieved model instance or None if not found.
        """

        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> list[TModels]:
        """
        Retrieves all records of the specified model from the database.

        Returns:
            list[TModels]: A list of model instances.
        """

        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, **conditions: dict[str, Any]) -> TModels | None:
        """
        Deletes a record that matches the given conditions.

        Args:
            **conditions (dict[str, Any]):
            A dictionary of filter conditions for deletion.

        Returns:
            TModels | None: The deleted object if found, otherwise None.
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
        Updates an existing record based on the specified filters.

        Args:
            filters (dict[str, Any]): A dictionary specifying the record to update.
            **values (Any): The field-value pairs to be updated.

        Returns:
            TModels | None: The updated object if found, otherwise None.
        """

        # Generate filter conditions
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
