from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .image import Image

if TYPE_CHECKING:
    from .local import Local


class GalleryLocalBase(SQLModel):
    local_id: Optional[int] = Field(
        default=None, foreign_key="local.id", primary_key=True
    )
    image_id: Optional[int] = Field(
        default=None, foreign_key="image.id", primary_key=True
    )
    arrangement: Optional[int] = Field(default=0)


class GalleryLocal(GalleryLocalBase, table=True):
    __tablename__ = "gallery_local"

    local: Optional["Local"] = Relationship(back_populates="images")
    image: Optional[Image] = Relationship(back_populates="gallery_local")


class GalleryLocalCreate(GalleryLocalBase):
    pass


class GalleryLocalRead(GalleryLocalBase):
    image: Optional[Image] = None
