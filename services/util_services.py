from typing import Type, TypeVar
from beanie import Document
from bson import ObjectId
from fastapi import HTTPException, status

from models.user_model import User
from utils.error_codes import ErrorCodes

T = TypeVar("T", bound=Document)


async def get_valid_document(id: str, model: Type[T]) -> T:
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCodes.BAD_OBJECT_ID.value,
        )

    document = await model.get(document_id=id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCodes.COLLECTION_NOT_FOUND.value,
        )

    return document


async def user_exists(username: str, email: str):
    existing_user = await User.find_one(User.username == username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    existing_user = await User.find_one(User.email == email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    return False
