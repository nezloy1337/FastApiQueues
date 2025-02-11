class ServiceError(Exception):
    """
    Base exception for errors occurring in the service layer.
    """


class DuplicateEntryError(ServiceError):
    """
    Exception raised when a duplicate entry violation occurs (e.g., UNIQUE constraint).
    """


class NotFoundError(ServiceError):
    """
    Exception raised when an object is not found in the database.
    """
