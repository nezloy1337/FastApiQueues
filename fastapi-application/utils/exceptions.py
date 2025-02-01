class ServiceError(Exception):
    """Базовое исключение для ошибок в сервисном слое."""

    message = "Ошибка сервиса"
    status_code = 500

    def __init__(self, detail: str = None):
        self.detail = detail or self.message
        super().__init__(self.detail)


class DuplicateEntryError(ServiceError):
    """Ошибка дублирования записи (например, нарушение UNIQUE)."""

    message = "Запись уже существует"
    status_code = 409


class NotFoundError(ServiceError):
    """Ошибка, если объект не найден в БД."""

    message = "Объект не найден"
    status_code = 404
