from typing import TYPE_CHECKING, Any, Callable, List, Type

from sqlalchemy.orm import selectinload

if TYPE_CHECKING:
    from core.types import TModels


class ConditionBuilder:
    """
    A utility class for dynamically generating filtering and loading conditions
    for SQLAlchemy queries.

    Attributes:
        model (Type[TModels]): The SQLAlchemy model associated with condition builder.
        filters (List[Any]): List of filter conditions for the query.
        options (List[Any]): List of loading options for relationships.
    """

    def __init__(self, model: Type["TModels"]):
        """
        Initializes the condition builder with a model.

        Args:
            model (Type[TModels]):
             The SQLAlchemy model for which conditions will be built.
        """
        self.model = model
        self.filters: List[Any] = []
        self.options: List[Any] = []

    def create_conditions(self, **conditions: Any) -> List[Any]:
        """
        Generates filtering conditions based on the provided keyword arguments.

        Args:
            **conditions (Any): Key-value pairs where the key is the model's field name
            and the value is the filtering value.

        Returns:
            List[Any]: A list of SQLAlchemy filter conditions.

        Raises:
            AttributeError: If the model does not contain the specified attribute.
        """

        for key, value in conditions.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no attribute '{key}'"
                )
            self.filters.append(column == value)
        return self.filters

    def create_options(self, *relation_names: str) -> List[Any]:
        """
        Generates loading options for SQLAlchemy relationships.

        Args:
            *relation_names (str): Names of related fields to be eagerly loaded.

        Returns:
            List[Any]: A list of SQLAlchemy options for relationship loading.

        Raises:
            AttributeError: If the model does not contain the specified relationship.
        """
        for name in relation_names:
            relation = getattr(self.model, name, None)
            if relation is None:
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no relation '{name}'"
                )
            self.options.append(selectinload(relation))
        return self.options


def get_condition_builder(
    model_type: Type["TModels"],
) -> Callable[..., ConditionBuilder]:
    """
    Provides a factory function to create a `ConditionBuilder` instance for a model.

    Args:
        model_type (Type[TModels]):
         The SQLAlchemy model for which the condition builder is created.

    Returns:
        Callable[..., ConditionBuilder]:
         A function that, when called, returns a `ConditionBuilder` instance.
    """

    def create_condition_builder() -> ConditionBuilder:
        """
        Creates and returns a `ConditionBuilder` instance for the specified model.

        Returns:
            ConditionBuilder: A new instance of `ConditionBuilder` for the given model.
        """
        return ConditionBuilder(model_type)

    return create_condition_builder
