class ServiceError(Exception):
    """ "
    Base exception for errors occurring in the service layer.

    Attributes:
        message (str): Default error message.
        status_code (int): HTTP status code associated with the error.
        detail (str): Specific error detail provided during initialization.
    """

    message = "Ошибка сервиса"
    status_code = 500

    def __init__(self, detail: str = None):
        self.detail = detail or self.message
        super().__init__(self.detail)


class DuplicateEntryError(ServiceError):
    """
    Exception raised when a duplicate entry violation occurs (e.g., UNIQUE constraint).

    Attributes:
        message (str): Default error message indicating the entry already exists.
        status_code (int): HTTP status code (409 Conflict).
    """

    message = "Запись уже существует"
    status_code = 409


class NotFoundError(ServiceError):
    """
    Exception raised when an object is not found in the database.

    Attributes:
        message (str): Default error message indicating the object was not found.
        status_code (int): HTTP status code (404 Not Found).
    """

    message = "Объект не найден"
    status_code = 404
