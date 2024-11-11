from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from api.deps.user_deps import get_current_user
from core.config import settings
from core.security import create_access_token, create_refresh_token
from models.user_model import User
from schemas.auth_schema import TokenSchema, TokenPayload
from schemas.user_schema import UserSchema
from services.user_services import UserServices

auth_router = APIRouter()


@auth_router.post(
    "/login", summary="Access creation and token refresh.", response_model=TokenSchema
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserServices.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password or Email."
        )

    # Access create and token refresh.
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.post(
    "/test-token",
    summary="Test to verify if token is valid.",
    response_model=UserSchema,
)
async def test_token(user: User = Depends(get_current_user)):
    return user


@auth_router.post("/refresh", summary="Reload token.", response_model=TokenSchema)
async def refresh_token(refresh_token_item: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token_item, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserServices.get_user_by_id_service(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user.",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }


@auth_router.post("/logout", summary="Logout user.")
async def logout(data: TokenSchema, user: User = Depends(get_current_user)):
    try:
        await UserServices.logout_service(data)
        return {"message": "Logout exitoso"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
