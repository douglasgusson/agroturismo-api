from typing import List

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.itinerary import Itinerary, ItineraryCreate, ItineraryRead
from ..models.itinerary_local import ItineraryLocal
from ..models.local import Local

router = APIRouter()


@router.post(
    "/", response_model=ItineraryRead, status_code=status.HTTP_201_CREATED
)
async def create_itinerary(
    *, itinerary_to_save: ItineraryCreate, session: Session = ActiveSession
):
    """
    Create a new itinerary
    """
    itinerary = Itinerary(**itinerary_to_save.dict())

    locals = session.exec(
        select(Local).where(Local.id.in_(itinerary_to_save.local_ids))
    ).all()

    if not locals or len(locals) != len(itinerary_to_save.local_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um ou mais locais não foram encontrados",
        )

    for local in locals:
        itinerary_local = ItineraryLocal(
            itinerary_id=itinerary.id,
            local_id=local.id,
            visit_order=itinerary_to_save.local_ids.index(local.id),
        )
        itinerary.itinerary_locals.append(itinerary_local)

    session.add(itinerary)
    session.commit()
    session.refresh(itinerary)

    return itinerary


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(*, id: int, session: Session = ActiveSession):
    """
    Delete an itinerary
    """
    itinerary = session.get(Itinerary, id)

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found"
        )

    session.delete(itinerary)
    session.commit()

    return None


@router.get("/public", response_model=List[Itinerary])
async def get_public_itineraries(
    *,
    local_ids: List[int] = Query(None),
    limit: int = 10,
    session: Session = ActiveSession
):
    """
    Get public itineraries
    """
    if local_ids:
        # return itineraries that contain any of the locals in local_ids
        itineraries = session.exec(
            select(Itinerary)
            .where(Itinerary.is_public)
            .where(Itinerary.id == ItineraryLocal.itinerary_id)
            .where(ItineraryLocal.local_id.in_(local_ids))
            .limit(limit)
        ).all()
    else:
        # return random public itineraries
        itineraries = session.exec(
            select(Itinerary).where(Itinerary.is_public).limit(limit)
        ).all()

    return itineraries
