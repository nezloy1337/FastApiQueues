from typing import Callable, Type

from fastapi import Depends

from core.registry import MODEL_REGISTRY

from ..types import TModels, TService
from .repository import get_repository_by_model


def get_service_by_model(
    model_cls: Type[TModels],
) -> Callable[..., TService]:  # сделать точную аннотацию
    """
     Accepts a model and retrieves (RepoClass, ServiceClass) from the registry.
    Returns a function (for FastAPI Depends) that creates a service instance.

    :param model_cls: The model class for which the service needs to be created.
    :return: A function that creates a service instance using FastAPI Depends.
    :rtype: Callable
    """
    service_cls, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_service(
        repository=Depends(get_repository_by_model(model_cls)),
    ) -> TService:
        """
        Internal function to create a service instance.

        :param repository: The repository instance retrieved via Depends.
        :type repository: Repository
        :return: An instance of the service class.
        :rtype: TService

        :note: This function is intended for use as the return
         value of `get_service_by_model`.
        """
        return service_cls(repository)

    return _create_service
