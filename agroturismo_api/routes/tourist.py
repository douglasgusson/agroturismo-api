from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.tourist import Tourist, TouristCreate, TouristRead

router = APIRouter()


@router.get("/", response_model=List[TouristRead])
async def list_tourists(*, session: Session = ActiveSession):
    tourists = session.exec(select(Tourist)).all()
    return tourists


@router.post("/", response_model=TouristRead, status_code=status.HTTP_201_CREATED)
async def create_tourist(
    *, tourist_to_save: TouristCreate, session: Session = ActiveSession
):
    tourist = Tourist(**tourist_to_save.dict())
    session.add(tourist)
    session.commit()
    session.refresh(tourist)
    return tourist
