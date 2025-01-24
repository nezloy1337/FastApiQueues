from typing import Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.base import TModels
from core.db_helper import db_helper
from core.factories.condition_builder import (
    ConditionBuilderFactory,
    get_condition_builder_factory,
)
from core.registry import MODEL_REGISTRY


def get_repository_by_model(model_cls: Type[TModels]):
    """
    Returns a dependency factory for creating a repository instance for the given model.
    """
    _, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_repository(
        session: AsyncSession = Depends(db_helper.session_getter),
        builder_factory: ConditionBuilderFactory = Depends(
            get_condition_builder_factory
        ),
    ):
        """
           Internal function to create a repository instance.

           This function is intended to be used internally by `get_repository_by_model`.
           It initializes the repository with a session and a condition builder specific
           to the given model.
           """
        condition_builder = builder_factory.create_for_model(model_cls)
        return repo_cls(session, condition_builder)

    return _create_repository
