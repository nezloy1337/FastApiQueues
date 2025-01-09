from pydantic import BaseModel


class TagSchema(BaseModel):
    name: str

class CreateTag(TagSchema):
    pass

class DeleteTag(TagSchema):
    pass

class CreateTagQueue(BaseModel):
    queue_id: int
    tag_id: int

