import cloudinary
import cloudinary.api
import cloudinary.uploader
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.config import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
)
from ..core.db import ActiveSession
from ..models.gallery_local import GalleryLocal
from ..models.image import Image

router = APIRouter()

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(*, image_id: int, session: Session = ActiveSession):
    image = session.get(Image, image_id)
    gallery = session.exec(
        select(GalleryLocal).where(GalleryLocal.image_id == image_id)
    ).first()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem não encontrada",
        )

    cloudinary_response = cloudinary.uploader.destroy(image.public_id)

    print(cloudinary_response)

    session.delete(gallery)
    session.delete(image)
    session.commit()
    return None
