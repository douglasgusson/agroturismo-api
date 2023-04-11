from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gallery_local import GalleryLocal


class ImageBase(SQLModel):
    url: str
    width: int
    height: int
    alt_text: Optional[str] = None


class Image(ImageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    gallery_local: Optional["GalleryLocal"] = Relationship(back_populates="image")


class ImageRead(ImageBase):
    pass
