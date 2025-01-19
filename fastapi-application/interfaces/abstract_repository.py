from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Dict, Any

from models.types import TModels


class AbstractRepository(ABC, Generic[TModels]):
    """Абстрактный класс репозитория, задающий интерфейс."""

    @abstractmethod
    async def create(self, obj_data: dict) -> TModels:
        """Создаёт новый объект."""
        pass

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Optional[TModels]:
        """Получает объект по ID."""
        pass

    @abstractmethod
    async def get_all(self) -> List[TModels]:
        """Получает все объекты."""
        pass

    @abstractmethod
    async def delete(self, **conditions: dict) -> bool:
        """Удаляет объекты, соответствующие условиям."""
        pass

    @abstractmethod
    async def patch(
        self, obj_unique_key: Dict[str, Any], **values: Any
    ) -> Optional[Dict[str, Any]]:
        """Обновляет объект с указанным уникальным ключом."""
        pass