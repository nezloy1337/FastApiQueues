from typing import Callable, Type

from fastapi import Depends

from core.registry import MODEL_REGISTRY

from ..base import BaseService
from ..types import TModels, TService
from .repository import get_repository_by_model


def get_service_by_model(
    model_cls: Type[TModels],
) -> Callable[..., TService]:
    """
    Retrieves the service class associated with the given model and
    returns a factory function that creates instances of the service.

    Args:
        model_cls (Type[TModels]): The model class used
        to look up the corresponding service.

    Returns:
        Callable[..., TService]: A function that, when called,
        returns an instance of the associated service.
    """

    # Retrieve the service and repository classes from the registry
    service_cls, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_service(
        repository=Depends(get_repository_by_model(model_cls)),
    ) -> BaseService[TModels, TService]:
        """
        Creates and returns an instance of the service class
        using the injected repository.

        Args:
            repository: The repository instance, injected via FastAPI Depends.

        Returns:
            TService: An instance of the associated service class.
        """
        return service_cls(repository)

    return _create_service
