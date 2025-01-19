from typing import Type

from core.base import TModels
from utils.condition_builder import ConditionBuilder


class ConditionBuilderFactory:
    """Фабрика, которая создает ConditionBuilder под конкретную модель."""
    @staticmethod
    def create_for_model(model: Type[TModels]) -> ConditionBuilder:
        return ConditionBuilder(model)


def get_condition_builder_factory():
    return ConditionBuilderFactory