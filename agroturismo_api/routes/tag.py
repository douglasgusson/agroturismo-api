from typing import List

from fastapi import APIRouter
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.tag import Tag, TagCreate, TagRead
from ..security import AuthenticatedAdminUser

router = APIRouter()


@router.get("/", response_model=List[TagRead])
def list_tags(*, session: Session = ActiveSession):
    tags = session.exec(select(Tag)).all()
    return tags


@router.post("/", response_model=TagRead, dependencies=[AuthenticatedAdminUser])
def create_tag(*, tag_to_save: TagCreate, session: Session = ActiveSession):
    tag = Tag.from_orm(tag_to_save)
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag


@router.get("/{id}", response_model=TagRead)
def get_tag(*, id: int, session: Session = ActiveSession):
    tag = session.get(Tag, id)
    return tag
