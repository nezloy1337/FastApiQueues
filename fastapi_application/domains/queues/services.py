from typing import Any

from fastapi import HTTPException
from starlette import status

from core.base.services import BaseService
from domains.queues import (
    Queue,
    QueueEntries,
    QueueEntriesRepository,
    QueueRepository,
    QueueTags,
    QueueTagsRepository,
)


class QueueEntryService(BaseService[QueueEntries, QueueEntriesRepository]):
    """
    Service layer for handling business logic related to queue entries.

    Attributes:
        repository (QueueEntriesRepository):
            The repository handling queue entry operations.
    """

    def __init__(
        self,
        repository: QueueEntriesRepository,
    ):
        super().__init__(repository)

    async def delete_all(self, filters: dict[str, Any]) -> bool:
        """
        Deletes all queue entries matching the given filters.

        Args:
            filters (Dict[str, Any]): Filtering criteria for deletion.

        Returns:
            bool: True if at least one entry was deleted.

        Raises:
            HTTPException: If no entries were found matching the criteria.
        """

        deleted_obj = await self.repository.delete_all(filters)
        if deleted_obj:
            return True

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not Found",
        )


class QueueTagService(BaseService[QueueTags, QueueTagsRepository]):
    """
    Service layer for handling business logic related to queue tags.

    Attributes:
        repository (QueueTagsRepository): The repository handling queue tag operations.
    """

    pass


class QueueService(BaseService[Queue, QueueRepository]):
    """
    Service layer for handling business logic related to queues.

    Attributes:
        repository (QueueRepository): The repository handling queue operations.
    """

    pass
