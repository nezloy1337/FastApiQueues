from core.factories import get_service_by_model
from domains.queues import QueueEntries, QueueTags, Queue
from domains.tags import Tags
from domains.users import User
"""
This module defines dependency factories for creating service instances for specific models.
These factories are designed for integration with FastAPI's dependency injection system.

Usage in FastAPI:
-----------------
These dependencies can be used in FastAPI routes as follows::

    @app.get("/users/")
    def get_users(service=Depends(get_user_service)):
        return service.get_all()

"""

get_user_service = get_service_by_model(User)

get_queue_entries_service = get_service_by_model(QueueEntries)

get_tags_service = get_service_by_model(Tags)

get_queue_tags_service = get_service_by_model(QueueTags)

get_queue_service = get_service_by_model(Queue)
