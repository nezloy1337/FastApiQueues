from core.factories import get_service_by_model
from domains.queues import Queue, QueueEntries, QueueTags
from domains.tags import Tags
from domains.users import User

"""
Dependency factories for service instances.

These factories create service instances for specific models and are 
designed for integration with FastAPI's dependency injection system.

Usage in FastAPI:
-----------------
These dependencies can be used in FastAPI routes as follows::

    @app.get("/users/")
    def get_users(service=Depends(get_user_service)):
        return service.get_all()
        
Factories:
    get_user_service: Creates a service instance for User.
    get_queue_entries_service: Creates a service instance for QueueEntries.
    get_tags_service: Creates a service instance for Tags.
    get_queue_tags_service: Creates a service instance for QueueTags.
    get_queue_service: Creates a service instance for Queue.
"""

get_user_service = get_service_by_model(User)
"""Creates a service instance for User."""

get_queue_entries_service = get_service_by_model(QueueEntries)
"""Creates a service instance for QueueEntries."""

get_tags_service = get_service_by_model(Tags)
"""Creates a service instance for Tags."""

get_queue_tags_service = get_service_by_model(QueueTags)
"""Creates a service instance for QueueTags."""

get_queue_service = get_service_by_model(Queue)
"""Creates a service instance for Queue."""
