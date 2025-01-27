from typing import Type

from utils.condition_builder import ConditionBuilder

from core.base import TModels


class ConditionBuilderFactory:
    """
    A factory for creating ConditionBuilder instances for specific models.
    """

    @staticmethod
    def create_for_model(model: Type[TModels]) -> ConditionBuilder:
        """
        Creates a ConditionBuilder for the given model.
        """
        return ConditionBuilder(model)


def get_condition_builder_factory():
    """
    Provides a ConditionBuilderFactory class.
    """
    return ConditionBuilderFactory
