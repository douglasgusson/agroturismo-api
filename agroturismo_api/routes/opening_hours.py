from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.opening_hours import OpeningHours, OpeningHoursCreate

router = APIRouter()


@router.get("/", response_model=List[OpeningHours])
async def get_opening_hours(*, local_id: int, session: Session = ActiveSession):
    """
    Get opening_hours by local_id
    """
    opening_hours = session.exec(
        select(OpeningHours)
        .where(OpeningHours.local_id == local_id)
        .order_by(OpeningHours.weekday)
    ).all()

    return opening_hours


@router.post("/", response_model=OpeningHours, status_code=status.HTTP_201_CREATED)
def create_opening_hours(
    *,
    session: Session = ActiveSession,
    opening_hours_to_save: OpeningHoursCreate,
):
    """
    Create a new opening_hours
    """
    opening_hours = OpeningHours(**opening_hours_to_save.dict())

    if opening_hours.weekday < 0 or opening_hours.weekday > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O dia da semana deve ser um número entre 0 e 6. 0 para domingo, 1 para segunda, etc.",
        )

    # check if there is already an opening_hours for this local and weekday
    opening_hours_already_exists = session.exec(
        select(OpeningHours)
        .where(OpeningHours.local_id == opening_hours.local_id)
        .where(OpeningHours.weekday == opening_hours.weekday)
    ).first()

    if opening_hours_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um horário de funcionamento para este local e dia da semana",
        )

    session.add(opening_hours)
    session.commit()
    session.refresh(opening_hours)
    return opening_hours


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opening_hours(*, session: Session = ActiveSession, id: int):
    """
    Delete opening_hours
    """
    opening_hours = session.get(OpeningHours, id)

    if not opening_hours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi encontrado horário de funcionamento com o id: {id}",
        )

    session.delete(opening_hours)
    session.commit()

    return None
