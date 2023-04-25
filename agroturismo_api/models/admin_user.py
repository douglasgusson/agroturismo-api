from typing import Optional

from sqlalchemy.orm import registry
from sqlmodel import Field, SQLModel

from .user import User

mapper_registry = registry()


class AdminUserBase(SQLModel):
    pass


@mapper_registry.mapped
class AdminUser(User, table=True):
    __tablename__ = "admin_user"

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class AdminUserCreate(AdminUserBase):
    username: str
    password: str


class AdminUserRead(AdminUserBase):
    id: int
    username: str
