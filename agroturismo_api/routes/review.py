from typing import List

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, desc, select

from ..core.db import ActiveSession
from ..models.review import Review, ReviewCreate, ReviewRead
from ..security import AuthenticatedTouristUser

router = APIRouter()


@router.post(
    "/",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[AuthenticatedTouristUser],
)
async def create_review(
    *, review_to_save: ReviewCreate, session: Session = ActiveSession
):
    """
    Create a new review
    """
    review = Review(**review_to_save.dict())

    session.add(review)
    session.commit()
    session.refresh(review)

    return review


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(*, id: int, session: Session = ActiveSession):
    """
    Delete a review
    """
    review = session.get(Review, id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada",
        )

    session.delete(review)

    session.commit()


@router.get("/", response_model=List[ReviewRead])
async def read_reviews(
    *,
    session: Session = ActiveSession,
    local_id: int = Query(None),
    tourist_id: int = Query(None)
):
    """
    Read reviews
    """
    reviews = session.exec(
        select(Review)
        .where(
            Review.local_id == local_id if local_id else True,
            Review.tourist_id == tourist_id if tourist_id else True,
        )
        .order_by(desc(Review.created_at))
    ).all()

    return reviews
