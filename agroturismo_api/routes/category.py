from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.category import Category, CategoryCreate, CategoryRead

router = APIRouter()


@router.get("/", response_model=List[CategoryRead])
def list_categories(*, session: Session = ActiveSession):
    """
    List all categories
    """
    categories = session.exec(select(Category)).all()
    return categories


@router.get("/{id}", response_model=CategoryRead)
def get_category_by_id(*, id: int, session: Session = ActiveSession):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )
    return category


@router.get("/find-by-slug/{slug}", response_model=CategoryRead)
def find_category_by_slug(*, slug: str, session: Session = ActiveSession):
    category = session.exec(select(Category).where(Category.slug == slug)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )
    return category


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_to_save: CategoryCreate, *, session: Session = ActiveSession
):
    category = Category(**category_to_save.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(*, id: int, session: Session = ActiveSession):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )
    session.delete(category)
    session.commit()
    return None


@router.patch("/{id}", response_model=CategoryRead)
def update_category(
    *, category_to_update: CategoryCreate, id: int, session: Session = ActiveSession
):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )

    patch_data = category_to_update.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.put("/{id}", response_model=CategoryRead)
def replace_category(
    *, category_to_replace: CategoryCreate, id: int, session: Session = ActiveSession
):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )

    category = Category(**category_to_replace.dict(), id=id)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category
