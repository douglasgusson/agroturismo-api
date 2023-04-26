from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from ..core.db import ActiveSession
from ..models.user import User, UserPasswordPatch, UserRead, get_password_hash
from ..security import (
    AuthenticatedFreshUser,
    AuthenticatedUser,
    RefreshToken,
    Token,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_user,
    validate_token,
)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(get_user, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha ou usuário incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "fresh": True},
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_token(form_data: RefreshToken):
    user = await validate_token(token=form_data.refresh_token)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "fresh": False},
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.get("/profile", response_model=UserRead)
async def get_profile_user(current_user: User = AuthenticatedUser):
    """
    Get profile from current user
    """
    return current_user


@router.patch(
    "/{user_id}/password/",
    response_model=UserRead,
    dependencies=[AuthenticatedFreshUser],
)
async def update_user_password(
    *,
    user_id: int,
    session: Session = ActiveSession,
    request: Request,
    user_patch: UserPasswordPatch,
):
    # Query the content
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Check the user can update the password
    current_user: User = get_current_user(request=request)
    if user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode atualizar esta senha de usuário",
        )

    if not user_patch.password == user_patch.password_confirm:
        raise HTTPException(
            status_code=400, detail="As senhas não correspondem"
        )

    # Update the password
    user.password = get_password_hash(user_patch.password)

    # Commit the session
    session.commit()
    session.refresh(user)
    return user
