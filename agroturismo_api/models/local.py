from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .category import Category
from .gallery_local import GalleryLocal, GalleryLocalRead
from .tag import Tag, TagRead
from .tag_local import TagLocal

if TYPE_CHECKING:
    from .itinerary_local import ItineraryLocal


class LocalBase(SQLModel):
    name: str
    slug: str = Field(unique=True, index=True)
    latitude: float
    longitude: float
    address: str
    website: Optional[str] = None
    phone: Optional[str] = None
    description: str
    main_category_id: int = Field(foreign_key="category.id")


class Local(LocalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    main_category: Optional[Category] = Relationship(back_populates="locals")
    images: Optional[GalleryLocal] = Relationship(back_populates="local")
    itinerary_locals: List["ItineraryLocal"] = Relationship(back_populates="local")
    tags: List[Tag] = Relationship(link_model=TagLocal)


class LocalCreate(LocalBase):
    tags_ids: List[int] = []


class LocalRead(LocalBase):
    id: int
    main_category: Optional[Category] = None
    images: List[GalleryLocalRead] = []
    tags: List[TagRead] = []
