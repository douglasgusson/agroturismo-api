from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .itinerary_local import ItineraryLocal


class ItineraryBase(SQLModel):
    is_public: bool = Field(default=False)


class Itinerary(ItineraryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tourist_id: int = Field(default=None, foreign_key="tourist.id")
    itinerary_locals: List[ItineraryLocal] = Relationship(
        back_populates="itinerary"
    )


class ItineraryCreate(ItineraryBase):
    local_ids: List[int]


class ItineraryRead(ItineraryBase):
    itinerary_locals: List[ItineraryLocal]
