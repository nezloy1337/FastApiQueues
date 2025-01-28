from typing import Any

from fastapi import HTTPException, status

from core.types import TModels, TRepositories
from utils.exception_handlers import handle_exception


class BaseService:
    """
    Base service implementing business logic using an abstract repository.

    :param repository: An instance of the repository handling operations on the model.
    """

    def __init__(
        self,
        repository: TRepositories,
    ):
        self.repository = repository

    @handle_exception
    async def create(self, obj_data: dict[str, Any]) -> TModels:
        """
        Creates a new object in the database.

        :param obj_data: Data for creating the object.
        :return: The created model object.
        """
        return await self.repository.create(obj_data)

    @handle_exception
    async def get_by_id(self, obj_id: int) -> TModels | None:
        """
        Retrieves an object by its identifier.

        :param obj_id: The unique identifier of the object.
        :return: The model object or None if not found.
        :raises HTTPException: If the object is not found.
        """
        obj = await self.repository.get_by_id(obj_id)

        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )
        return obj

    @handle_exception
    async def get_all(self) -> list[TModels]:
        """
        Retrieves a list of all objects.

        :return: A list of model objects.
        """
        return await self.repository.get_all()

    @handle_exception
    async def delete(self, filters: dict[str, Any]) -> bool:
        """
        Deletes an object that matches the specified conditions.

        :param filters: Search filters for the object(s)
        (e.g., {"queue_id": 1, "user_id": 2}).
        :return: True if the object was successfully deleted.
        :raises HTTPException: If the object is not found.
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
        Updates object(s) matching the specified filters and returns the updated data.

        :param filters: Search filters for the object(s) (e.g., {"id": 1}).
        :param values: Values to update (e.g., name="New Name").
        :return: A dictionary of the updated data.
        :raises HTTPException: If the object is not found.
        """
        patched_obj = await self.repository.patch(filters, **values)
        if patched_obj:
            return patched_obj

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )
