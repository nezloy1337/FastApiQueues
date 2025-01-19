from typing import Type

from fastapi import Depends

from core.registry import MODEL_REGISTRY
from models import TModels
from .repository import get_repository_by_model


def get_service_by_model(model_cls: Type[TModels]) -> object:
    """
    Принимает модель, находит в реестре (RepoClass, ServiceClass).
    Возвращает функцию (для Depends), которая создаст экземпляр сервиса.
    """
    service_cls, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_service(
        # Берём репозиторий через Depends, используя фабрику выше
        repository=Depends(get_repository_by_model(model_cls)),
    ):
        return service_cls(repository)

    return _create_service
