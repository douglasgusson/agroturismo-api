from typing import Optional

from sqlalchemy.orm import registry
from sqlmodel import Field, SQLModel

from .user import User

mapper_registry = registry()


class TouristBase(SQLModel):
    name: str
    email: str


@mapper_registry.mapped
class Tourist(User, TouristBase, table=True):
    __tablename__ = "tourist"

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    __mapper_args__ = {
        "polymorphic_identity": "tourist",
    }


class TouristCreate(TouristBase):
    username: str
    password: str


class TouristRead(TouristBase):
    id: int
    username: str
