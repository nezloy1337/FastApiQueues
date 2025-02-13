from typing import Any, Generic

from fastapi import HTTPException, status

from core.types import TModels, TRepositories


class BaseService(Generic[TModels, TRepositories]):
    """
    A base service layer that provides business logic
    abstraction over repository operations.

    This service acts as an intermediary between API routes and repositories, ensuring
    that business rules are enforced consistently.

    Attributes:
        repository (TRepositories):
        The repository instance managing the model's database operations.
    """

    def __init__(
        self,
        repository: TRepositories,
    ):
        """
        Initializes the service with a repository instance.

        Args:
            repository (TRepositories):
            The repository instance that provides database access.
        """
        self.repository = repository

    async def create(
        self,
        obj_data: dict[str, Any],
    ) -> TModels:
        """
        Creates a new object and persists it in the database.

        Args:
            obj_data (dict[str, Any]):
            A dictionary containing field values for the new object.

        Returns:
            TModels: The created model instance.
        """
        return await self.repository.create(obj_data)

    async def get_by_id(
        self,
        obj_id: int,
    ) -> TModels:
        """
        Retrieves an object by its unique identifier.

        Args:
            obj_id (int): The unique identifier of the object.

        Returns:
            TModels: The retrieved model object.

        Raises:
            HTTPException: If the object is not found.
        """

        obj = await self.repository.get_by_id(obj_id)

        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )

        return obj

    async def get_all(self) -> list[TModels]:
        """
        Retrieves all objects managed by the repository.

        Returns:
            list[TModels]: A list of model instances.
        """

        return await self.repository.get_all()

    async def delete(
        self,
        filters: dict[str, Any],
    ) -> bool:
        """
        Deletes an object matching the specified filters.

        Args:
            filters (dict[str, Any]): A dictionary specifying the criteria for deletion
            (e.g., {"queue_id": 1, "user_id": 2}).

        Returns:
            bool: True if the object was successfully deleted.

        Raises:
            HTTPException: If the object is not found.
        """

        deleted_obj = await self.repository.delete(**filters)
        if deleted_obj:
            return True

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )

    async def patch(
        self,
        filters: dict[str, Any],
        **values: Any,
    ) -> dict[str, Any]:
        """
        Updates an object based on specified filters and returns the updated data.

        Args:
            filters (dict[str, Any]): Criteria for identifying the object(s) to update
            (e.g., {"id": 1}).
            **values (Any): Key-value pairs specifying fields to update
            (e.g., name="New Name").

        Returns:
            dict[str, Any]: The updated object data.

        Raises:
            HTTPException: If the object is not found.
        """

        patched_obj = await self.repository.patch(filters, **values)
        if patched_obj:
            return patched_obj

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )
