from typing import Type, List, Any

from sqlalchemy.orm import selectinload

from models import TModels


class ConditionBuilder:
    """Класс для построения условий и опций запросов."""

    def __init__(self, model: Type[TModels]):
        self.model = model
        self.filters: List[Any] = []
        self.options: List[Any] = []

    def create_conditions(self, **conditions: Any) -> List[Any]:
        """Добавляет фильтры на основе переданных условий."""
        for key, value in conditions.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise AttributeError(f"Model '{self.model.__name__}' has no attribute '{key}'")
            self.filters.append(column == value)
        return self.filters

    def create_options(self, *relation_names: str) -> List[Any]:
        """Добавляет опции для предзагрузки связанных данных."""
        for name in relation_names:
            relation = getattr(self.model, name, None)
            if relation is None:
                raise AttributeError(f"Model '{self.model.__name__}' has no relation '{name}'")
            self.options.append(selectinload(relation))
        return self.options


def get_condition_builder(repository_type):
    def create_condition_builder() -> ConditionBuilder:
        return ConditionBuilder(repository_type)
    return create_condition_builder
