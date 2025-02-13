from typing import Type

from utils.condition_builder import ConditionBuilder


class ConditionBuilderFactory[TModels]:
    """
    A factory class for creating `ConditionBuilder` instances for specific models.y.
    """

    @staticmethod
    def create_for_model(model: Type[TModels]) -> ConditionBuilder:
        """
        Creates and returns a `ConditionBuilder` instance for the specified model.

        Args:
            model (Type[TModels]): The SQLAlchemy model class
            for which to create a condition builder.

        Returns:
            ConditionBuilder: A new instance of 'ConditionBuilder'
            for the specified model.
        """
        return ConditionBuilder(model)


def get_condition_builder_factory() -> Type[ConditionBuilderFactory]:
    """
    Provides access to the `ConditionBuilderFactory` class.

    Returns:
        Type[ConditionBuilderFactory]: The `ConditionBuilderFactory` class.
    """

    return ConditionBuilderFactory
