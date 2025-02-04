from core.base.services import BaseService
from domains.tags import Tags, TagsRepository


class TagsService(BaseService[Tags, TagsRepository]):
    """
    Service layer for handling business logic related to tags.

    Attributes:
        repository (TagsRepository): The repository handling tag operations.
    """

    pass
