from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt
import bcrypt
from core.config import settings
import logging
from models.token_model import BlacklistToken

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash almacenado
    """
    try:
        # Convertir strings a bytes para bcrypt
        if isinstance(plain_password, str):
            plain_password = plain_password.encode("utf-8")
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


async def verify_token(token: str) -> bool:
    """
    Verifica si el token está en la lista negra
    """
    blacklsted = await BlacklistToken.find_one({"token": token})
    if blacklsted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ha sido revocado",
        )
    return True


def get_password_hash(password: str) -> str:
    """
    Genera un nuevo hash para la contraseña proporcionada
    """
    try:
        if isinstance(password, str):
            password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf-8")
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict):
    return create_token(
        data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(data: dict):
    return create_token(
        data, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )
