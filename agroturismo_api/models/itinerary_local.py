from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .local import Local

if TYPE_CHECKING:
    from .itinerary import Itinerary


class ItineraryLocalBase(SQLModel):
    itinerary_id: int = Field(
        default=None, foreign_key="itinerary.id", primary_key=True
    )
    local_id: int = Field(
        default=None, foreign_key="local.id", primary_key=True
    )
    visit_order: int = Field(default=None)


class ItineraryLocal(ItineraryLocalBase, table=True):
    __tablename__ = "itinerary_local"

    itinerary: Optional["Itinerary"] = Relationship(
        back_populates="itinerary_locals"
    )
    local: Local = Relationship(back_populates="itinerary_locals")


class ItineraryLocalRead(ItineraryLocalBase):
    pass
