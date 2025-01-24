from typing import Type, List, Any

from sqlalchemy.orm import selectinload

from core.base import TModels


class ConditionBuilder:
    """
    A class for constructing query conditions and options.
    """

    def __init__(self, model: Type[TModels]):
        self.model = model
        self.filters: List[Any] = []
        self.options: List[Any] = []

    def create_conditions(self, **conditions: Any) -> List[Any]:
        """
        Creates filter instances for sqlalchemy .filter() func based on the provided conditions.

        :param conditions: Key-value pairs where keys are model attributes and values are filter criteria.
        :return: A list of SQLAlchemy filter conditions.
        :raises AttributeError: If a specified key does not exist in the model.
        """
        for key, value in conditions.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise AttributeError(f"Model '{self.model.__name__}' has no attribute '{key}'")
            self.filters.append(column == value)
        return self.filters

    def create_options(self, *relation_names: str) -> List[Any]:
        """
        Creates options  instances for sqlalchemy .selectinload() or other func for preloading related data.

        :param relation_names: Names of related attributes to preload.
        :return: A list of SQLAlchemy `selectinload` options.
        :raises AttributeError: If a specified relation name does not exist in the model.
        """
        for name in relation_names:
            relation = getattr(self.model, name, None)
            if relation is None:
                raise AttributeError(f"Model '{self.model.__name__}' has no relation '{name}'")
            self.options.append(selectinload(relation))
        return self.options


def get_condition_builder(repository_type):
    """
    Creates a factory function for initializing a `ConditionBuilder` for a specific model.
    :param repository_type: The SQLAlchemy model associated with the repository.
    :return: A callable that creates an instance of `ConditionBuilder`.
    """

    def create_condition_builder() -> ConditionBuilder:
        """
        Initializes a `ConditionBuilder` for the specified repository type.

        :return: An instance of `ConditionBuilder` tied to the given model.
        """
        return ConditionBuilder(repository_type)

    return create_condition_builder
