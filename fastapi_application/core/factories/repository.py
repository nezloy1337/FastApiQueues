from typing import Annotated, Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.registry import MODEL_REGISTRY
from core.types import TModels, TRepositories
from utils import get_condition_builder
from utils.condition_builder import ConditionBuilder


def get_repository_by_model(model_cls: Type[TModels]) -> Callable[..., TRepositories]:
    """
    Retrieves the repository class associated with the given model and returns
    a factory function that creates instances of the repository.

    Args:
        model_cls (Type[TModels]): The model class used
        to look up the corresponding repository.

    Returns:
        Callable[..., TRepositories]: A function that, when called,
        returns an instance of the associated repository.
    """

    # Retrieve the repository class from the registry
    _, repo_cls = MODEL_REGISTRY[model_cls]

    def _create_repository(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        condition_builder: Annotated[
            ConditionBuilder,
            Depends(get_condition_builder(model_cls)),
        ],
    ) -> TRepositories:
        """
        Creates and returns an instance of the repository
        class using injected dependencies.

        Args:
            session (AsyncSession): The database session, injected via FastAPI Depends.
            condition_builder (ConditionBuilder): The condition builder
            for query filtering, injected via Depends.

        Returns:
            TRepositories: An instance of the associated repository class.
        """
        return repo_cls(session, condition_builder)

    return _create_repository
