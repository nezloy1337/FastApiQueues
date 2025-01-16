from factories import ServiceFactory
from repositories import (
    UserRepository,
    QueueRepository,
    QueueTagsRepository,
    QueueEntriesRepository,
    TagsRepository,
)
from services import (
    UserService,
    QueueEntryService,
    TagsService,
    QueueService,
    QueueTagService,
)


get_user_service = ServiceFactory.create(
    UserService,
    UserRepository,
)

get_queue_entries_service = ServiceFactory.create(
    QueueEntryService,
    QueueEntriesRepository,
)

get_tags_service = ServiceFactory.create(
    TagsService,
    TagsRepository,
)

get_queue_tags_service = ServiceFactory.create(
    QueueTagService,
    QueueTagsRepository,
)

get_queue_service = ServiceFactory.create(
    QueueService,
    QueueRepository,
)
