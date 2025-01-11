from pydantic import BaseModel


class TagBase(BaseModel):
    name: str

class CreateTag(TagBase):
    pass

class DeleteTag(TagBase):
    pass

class GetTag(TagBase):
    id: int

class CreateTagQueue(BaseModel):
    queue_id: int
    tag_id: int

