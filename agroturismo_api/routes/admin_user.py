from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from ..core.db import ActiveSession
from ..models.admin_user import AdminUser, AdminUserCreate, AdminUserRead
from ..security import validate_username

router = APIRouter()


@router.get("/", response_model=List[AdminUserRead])
async def list_admin_users(*, session: Session = ActiveSession):
    tourists = session.exec(select(AdminUser)).all()
    return tourists


@router.post(
    "/", response_model=AdminUserRead, status_code=status.HTTP_201_CREATED
)
async def create_admin_user(
    *, admin_user_to_save: AdminUserCreate, session: Session = ActiveSession
):
    validate_username(admin_user_to_save.username)

    admin_user = AdminUser(**admin_user_to_save.dict())
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    return admin_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin_user(*, id: int, session: Session = ActiveSession):
    admin_user = session.get(AdminUser, id)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário admin não encontrado",
        )
    session.delete(admin_user)
    session.commit()
    return None
