from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.special_opening_hours import (
    SpecialOpeningHours,
    SpecialOpeningHoursCreate,
)

router = APIRouter()


@router.get("/", response_model=List[SpecialOpeningHours])
async def get_special_opening_hours(*, local_id: int, session: Session = ActiveSession):
    """
    Get special_opening_hours by local_id
    """
    special_opening_hours = session.exec(
        select(SpecialOpeningHours).where(
            SpecialOpeningHours.local_id == local_id
            and SpecialOpeningHours.opening_date >= datetime.today()
        )
    ).all()

    return special_opening_hours


@router.post(
    "/",
    response_model=SpecialOpeningHours,
    status_code=status.HTTP_201_CREATED,
)
def create_special_opening_hours(
    *,
    session: Session = ActiveSession,
    special_opening_hours: SpecialOpeningHoursCreate,
):
    """
    Create a new special_opening_hours
    """
    special_opening_hours = SpecialOpeningHours(**special_opening_hours.dict())
    session.add(special_opening_hours)
    session.commit()
    session.refresh(special_opening_hours)
    return special_opening_hours


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_special_opening_hours(*, session: Session = ActiveSession, id: int):
    """
    Delete a special_opening_hours
    """
    special_opening_hours = session.get(SpecialOpeningHours, id)

    if not special_opening_hours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi encontrado horário especial com o id: {id}",
        )

    session.delete(special_opening_hours)
    session.commit()

    return None
