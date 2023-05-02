from typing import List, Union

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel import Session, or_, select

from ..core.db import ActiveSession
from ..models.category import Category, CategoryRead
from ..models.local import Local, LocalRead
from ..models.tag import Tag, TagRead

router = APIRouter()


class SearchResults(BaseModel):
    locals: List[LocalRead]
    categories: List[CategoryRead]
    tags: List[TagRead]


@router.get("/", response_model=SearchResults)
async def search(
    *,
    query: str = Query(None),
    category_id: Union[int, None] = Query(None),
    tags: List[str] = Query(None),
    session: Session = ActiveSession,
):
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search text is required",
        )

    category_text_search_condition = or_(
        Category.name.ilike(f"%{query}%"),
        Category.slug.ilike(f"%{query}%"),
    )

    local_text_search_condition = or_(
        Local.name.ilike(f"%{query}%"),
        Local.slug.ilike(f"%{query}%"),
        Local.description.ilike(f"%{query}%"),
        Local.address.ilike(f"%{query}%"),
        Local.website.ilike(f"%{query}%"),
        Local.phone.ilike(f"%{query}%"),
        Local.main_category.has(category_text_search_condition),
    )

    tag_text_search_condition = or_(
        Tag.content.ilike(f"%{query}%"),
    )

    locals = session.exec(
        select(Local).where(local_text_search_condition).order_by(Local.name)
    ).all()

    categories = session.exec(
        select(Category).where(category_text_search_condition).order_by(Category.name)
    ).all()

    tags = session.exec(
        select(Tag).where(tag_text_search_condition).order_by(Tag.content)
    ).all()

    return SearchResults(locals=locals, categories=categories, tags=tags)
