from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    slug: str

class CategoryIncoming(BaseModel):
    name: str
