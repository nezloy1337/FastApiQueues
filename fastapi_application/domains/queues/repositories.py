from typing import Any

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.base.repository import BaseRepository
from core.exceptions import DuplicateEntryError
from domains.queues import Queue, QueueEntries, QueueTags
from utils.condition_builder import ConditionBuilder


class QueueRepository(BaseRepository[Queue]):
    """
    Repository for managing Queue-related database operations.

    Attributes:

        session (AsyncSession): The database session.
        condition_builder (ConditionBuilder): Utility for building query conditions.
    """

    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            Queue,
            session,
            condition_builder,
        )

    async def get_by_id(self, queue_id: int) -> Queue | None:
        """
        Retrieves a queue by its unique identifier.

        Args:
            queue_id (int): The ID of the queue to retrieve.

        Returns:
            Queue | None: The queue instance if found, otherwise None.
        """

        query = (
            select(Queue)
            .where(Queue.id == queue_id)
            .options(
                selectinload(Queue.entries).selectinload(QueueEntries.user),
                selectinload(Queue.queue_tags),  # Загружаем связанные теги
            )
        )

        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self) -> list[Queue]:
        """
        Retrieves all queue records.

        Returns:
            list[Queue]: A list of all queue instances.
        """

        query = select(Queue).options(
            selectinload(Queue.queue_tags),
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())


class QueueEntriesRepository(BaseRepository[QueueEntries]):
    """
    Repository for managing QueueEntries-related database operations.

    Attributes:
        session (AsyncSession): The database session.
        condition_builder (ConditionBuilder): Utility for building query conditions.
    """

    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(QueueEntries, session, condition_builder)

    async def delete_all(self, filters: dict[str, Any]) -> QueueEntries | None:
        """
        Deletes all queue entries matching the provided filters.

        Args:
            filters (Dict[str, Any]): Filtering criteria for deletion.

        Returns:
            QueueEntries | None: The deleted queue entry if found, otherwise None.
        """
        query_conditions = self.condition_builder.create_conditions(**filters)

        stmt = delete(self.model).filter(and_(*query_conditions)).returning(self.model)

        result = await self.session.execute(stmt)
        deleted_obj = result.scalars().first()
        if deleted_obj:
            await self.session.commit()
        return deleted_obj

    async def create(self, obj_data: dict[str, Any]) -> QueueEntries:
        """
        Creates a new queue entry in the database.

        Args:
            obj_data (Dict[str, Any]): The data for creating the queue entry.

        Returns:
            QueueEntries: The created queue entry.

        Raises:
            DuplicateEntryError: If an entry with the same
            user_id and queue_id already exists.
        """

        filters = self.condition_builder.create_conditions(
            user_id=obj_data.get("user_id"),
            queue_id=obj_data.get("queue_id"),
        )

        queue_entry = await self.session.execute(select(self.model).filter(*filters))
        if queue_entry.scalar_one_or_none():
            raise DuplicateEntryError

        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()

        return obj


class QueueTagsRepository(BaseRepository[QueueTags]):
    """
    Repository for managing QueueTags-related database operations.

    Attributes:
        session (AsyncSession): The database session.
        condition_builder (ConditionBuilder): Utility for building query conditions.
    """

    def __init__(self, session: AsyncSession, condition_builder: ConditionBuilder):
        super().__init__(
            QueueTags,
            session,
            condition_builder,
        )
