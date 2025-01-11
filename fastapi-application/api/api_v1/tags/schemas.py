from typing import Optional

from pydantic import BaseModel

class TagIdMixin(BaseModel):
    id: int


class TagBase(BaseModel):
    name: str


class CreateTag(TagBase):
    pass


class DeleteTag(TagBase, TagIdMixin):
    pass


class PatchTag(TagBase):
    pass



class GetTag(TagBase, TagIdMixin):
    pass


class CreateTagQueue(BaseModel):
    queue_id: int
    tag_id: int

