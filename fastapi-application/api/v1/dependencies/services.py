
from factories.get_service import ServiceFactory
from repositories.queue import QueueRepository
from repositories.queue_entry import QueueEntriesRepository
from repositories.queue_tags import QueueTagsRepository
from repositories.tags import TagsRepository
from repositories.user import UserRepository
from services.services import UserService, QueueEntryService, TagsService, QueueService, QueueTagService


get_user_service = ServiceFactory.create(UserService, UserRepository)
get_queue_entries_service = ServiceFactory.create(QueueEntryService, QueueEntriesRepository)
get_tags_service = ServiceFactory.create(TagsService, TagsRepository)
get_queue_tags_service = ServiceFactory.create(QueueTagService, QueueTagsRepository)
get_queue_service = ServiceFactory.create(QueueService, QueueRepository)
