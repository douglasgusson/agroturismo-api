from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    content: str

class TagIncoming(BaseModel):
    content: str
