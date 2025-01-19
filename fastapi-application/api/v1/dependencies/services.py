from factories.service import get_service_by_model
from models import User, QueueEntries, Tags, Queue, QueueTags

get_user_service = get_service_by_model(User)

get_queue_entries_service = get_service_by_model(QueueEntries)

get_tags_service = get_service_by_model(Tags)

get_queue_tags_service = get_service_by_model(QueueTags)

get_queue_service = get_service_by_model(Queue)
