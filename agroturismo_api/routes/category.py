from typing import List

from fastapi import APIRouter, status

from ..models.category import Category, CategoryIncoming

router = APIRouter()


@router.get("/", response_model=List[Category])
def list_categories():
    """
    List all categories
    """
    return []

@router.get("/{id}", response_model=Category)
def get_category_by_id():
    return None

@router.get("/{slug}", response_model=Category)
def get_category_by_slug():
    return None

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category_to_save: CategoryIncoming):
    return Category(id=1, *category_to_save)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int):
    return None


@router.patch("/{id}", response_model=Category)
def update_category(id: int, category_patch: Category):
    return category_patch
