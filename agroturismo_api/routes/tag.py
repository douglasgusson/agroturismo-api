from typing import List

from fastapi import APIRouter

from ..models.tag import Tag, TagIncoming

router = APIRouter()


@router.get("/", response_model=List[Tag])
def list_tags():
    return []


@router.post("/", response_model=Tag)
def create_tag(tag_to_save: TagIncoming):
    return Tag(id=1, content=tag_to_save.content)

