
from factories.get_service import get_service
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


get_user_service = get_service(
    UserService,
    UserRepository,
)

get_queue_entries_service = get_service(
    QueueEntryService,
    QueueEntriesRepository,
)

get_tags_service = get_service(
    TagsService,
    TagsRepository,
)

get_queue_tags_service = get_service(
    QueueTagService,
    QueueTagsRepository,
)

get_queue_service = get_service(
    QueueService,
    QueueRepository,
)
