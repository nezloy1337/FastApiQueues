from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_condition_builder
from utils.condition_builder import ConditionBuilder

from core.db_helper import db_helper
from core.registry import MODEL_REGISTRY
from core.types import TModels


def get_repository_by_model(model_cls: Type[TModels]):
    """
    Returns a dependency factory for creating a repository instance for the given model.
    """
    _, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_repository(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        condition_builder: Annotated[
            ConditionBuilder,
            Depends(get_condition_builder(model_cls)),
        ],
    ):
        """
        Internal function to create a repository instance.

        This function is intended to be used internally by `get_repository_by_model`.
        It initializes the repository with a session and a condition builder specific
        to the given model.
        """

        return repo_cls(session, condition_builder)

    return _create_repository
