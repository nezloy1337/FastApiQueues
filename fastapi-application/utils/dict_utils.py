from typing import Dict, Any


def combine_dict_with_named_params(data: Dict[str, Any], **extra: Any) -> Dict[str, Any]:
    """Возвращает новый словарь, объединяющий исходный словарь с дополнительными параметрами."""
    return {**data, **extra}