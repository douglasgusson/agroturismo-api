from sqlmodel import Field, SQLModel


class CategoryLocalBase(SQLModel):
    category_id: int = Field(default=None, foreign_key="category.id", primary_key=True)
    local_id: int = Field(default=None, foreign_key="local.id", primary_key=True)


class CategoryLocal(CategoryLocalBase, table=True):
    __tablename__ = "category_local"


class CategoryLocalRead(CategoryLocalBase):
    pass
