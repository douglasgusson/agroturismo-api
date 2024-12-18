from typing import Annotated, List, Union

import cloudinary
import cloudinary.api
import cloudinary.uploader
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from sqlmodel import Session, or_, select, case

from ..core.config import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
)
from ..core.db import ActiveSession
from ..models.cost import Cost
from ..models.gallery_local import GalleryLocal
from ..models.image import Image
from ..models.local import Local, LocalCreate, LocalRead

router = APIRouter()

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


@router.get("/", response_model=List[LocalRead])
async def list_locals(
    *,
    search: str = Query(None),
    ids: List[int] = Query(None),
    category_id: Union[int, None] = Query(None),
    tags: List[str] = Query(None),
    session: Session = ActiveSession,
):
    text_search_condition = or_(
        Local.name.ilike(f"%{search}%"),
        Local.description.ilike(f"%{search}%"),
        Local.address.ilike(f"%{search}%"),
        Local.website.ilike(f"%{search}%"),
        Local.phone.ilike(f"%{search}%"),
    )

    ordering = case(
        {_id: index for index, _id in enumerate(ids)},
        value=Local.id,
    ) if ids else Local.name

    locals = session.exec(
        select(Local)
        .where(
            Local.main_category_id == category_id if category_id else True,
            Local.id.in_(ids) if ids else True,
            text_search_condition if search else True,
            # Local.tags.any(tags) if tags else True,
        )
        .order_by(ordering)
    ).all()
    return locals


@router.post("/", response_model=LocalRead, status_code=status.HTTP_201_CREATED)
async def create_local(*, local_to_save: LocalCreate, session: Session = ActiveSession):
    local = Local(**local_to_save.dict())
    session.add(local)
    session.commit()
    session.refresh(local)
    return local


@router.get("/{id}", response_model=LocalRead)
async def get_local_by_id(*, id: int, session: Session = ActiveSession):
    local = session.get(Local, id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )
    return local


@router.get("/find-by-slug/{slug}", response_model=LocalRead)
async def find_local_by_slug(*, slug: str, session: Session = ActiveSession):
    local = session.exec(select(Local).where(Local.slug == slug)).first()
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )
    return local


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_local(*, id: int, session: Session = ActiveSession):
    local = session.get(Local, id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )
    session.delete(local)
    session.commit()
    return None


@router.patch("/{id}", response_model=LocalRead)
async def update_local(
    *, id: int, local_patch: LocalCreate, session: Session = ActiveSession
):
    local = session.get(Local, id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )

    patch_data = local_patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(local, key, value)

    session.add(local)
    session.commit()
    session.refresh(local)
    return local


@router.put("/{id}", response_model=LocalRead)
async def replace_local(
    *, id: int, local_to_update: LocalCreate, session: Session = ActiveSession
):
    local = session.get(Local, id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )

    local = Local(**local_to_update.dict(), id=id)

    session.add(local)
    session.commit()
    session.refresh(local)
    return local


@router.post("/add-images/{local_id}", response_model=LocalRead)
async def create_local_gallery(
    *,
    image_files: Annotated[
        list[UploadFile],
        File(description="Multiple image files as UploadFile"),
    ],
    local_id: int,
    session: Session = ActiveSession,
):
    local = session.get(Local, local_id)
    if not local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Local não encontrado",
        )

    for index, image_file in enumerate(image_files):
        filename_without_extension = image_file.filename.split(".")[0]
        cloudinary_response = cloudinary.uploader.upload(
            folder=f"agroturismo/locais/{local.slug}",
            public_id=filename_without_extension,
            file=image_file.file,
            overwrite=True,
        )

        image = Image(
            url=cloudinary_response["url"],
            width=cloudinary_response["width"],
            height=cloudinary_response["height"],
            public_id=cloudinary_response["public_id"],
        )

        session.add(image)
        session.commit()

        gallery_local = GalleryLocal(
            local_id=local.id, image_id=image.id, arrangement=index
        )

        session.add(gallery_local)
        session.commit()

    session.add(local)
    session.commit()
    session.refresh(local)

    return local
