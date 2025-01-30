from core.base.services import BaseService
from domains.tags import Tags, TagsRepository


class TagsService(BaseService[Tags, TagsRepository]):
    pass
