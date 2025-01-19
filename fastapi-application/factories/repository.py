from typing import Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.registry import MODEL_REGISTRY
from factories.condition_builder import (
    ConditionBuilderFactory,
    get_condition_builder_factory,
)
from models import TModels


def get_repository_by_model(model_cls: Type[TModels]):
    """
    Принимает модель, внутри смотрит в реестр, находит соответствующий класс репозитория.
    Возвращает функцию (для Depends), которая создаст экземпляр репозитория.
    """
    _, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_repository(
        session: AsyncSession = Depends(db_helper.session_getter),
        builder_factory: ConditionBuilderFactory = Depends(
            get_condition_builder_factory
        ),
    ):
        condition_builder = builder_factory.create_for_model(model_cls)
        return repo_cls(session, condition_builder)

    return _create_repository
