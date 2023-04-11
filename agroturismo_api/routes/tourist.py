from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.tourist import Tourist, TouristRead

router = APIRouter()


@router.get("/", response_model=List[TouristRead])
async def list_tourists(*, session: Session = ActiveSession):
    tourists = session.exec(select(Tourist)).all()
    return tourists
