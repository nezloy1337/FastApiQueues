from typing import Any

from fastapi import HTTPException
from starlette import status

from core.base.services import BaseService
from domains.queues import Queue, QueueEntry, QueueRepository, QueueTags
from utils.exception_handlers import handle_exception


class QueueEntryService(BaseService[QueueEntry]):
    def __init__(
        self,
        repository: QueueRepository,
    ):
        super().__init__(repository)

    @handle_exception
    async def delete_all(self, filters: dict[str, Any]) -> bool:
        """
        Удаляет объекты, соответствующий условиям.

        :param filters: Фильтры поиска объектов
        (например, {"queue_id": 1,"user_id":2}).
        :return: True, если объект успешно удалён.
        :raises HTTPException: Если объект не найден.
        """
        deleted_obj = await self.repository.delete_all(filters)
        if deleted_obj:
            return True

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not Found",
        )


class QueueTagService(BaseService[QueueTags]):
    pass


class QueueService(BaseService[Queue]):
    pass
