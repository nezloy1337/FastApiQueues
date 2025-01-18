from typing import Type

from models import TModels
from utils.condition_builder import ConditionBuilder


class ConditionBuilderFactory:

    def create_for_model(self, model: Type[TModels]) -> ConditionBuilder:
        return ConditionBuilder(model)

def get_condition_builder_factory() -> ConditionBuilderFactory:
    return ConditionBuilderFactory()