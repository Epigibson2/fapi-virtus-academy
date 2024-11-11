from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.user_deps import get_current_user
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from services.user_services import UserServices
from models.user_model import User
from utils.permission_utils import require_permission

users_router = APIRouter()


@users_router.post("/", summary="Se crea un nuevo usuario")
async def create_user(payload: UserCreate):
    try:
        result = await UserServices.create_user_service(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@users_router.get("/me", summary="Get the user logged in.")
async def get_me(user: User = Depends(get_current_user)):
    try:
        if user:
            # Convertir los campos problemáticos
            user_dict = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "active": user.active,
                "roles": [
                    str(role.id) if hasattr(role, "id") else str(role)
                    for role in user.roles
                ],
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "followers": [str(f) for f in user.followers],
                "following": [str(f) for f in user.following],
                "profile_picture": user.profile_picture,
                "bio": user.bio,
                "location": user.location,
                "website": user.website,
                "post_count": user.post_count,
                "followers_count": user.followers_count,
                "following_count": user.following_count,
                "private_account": user.private_account,
                "verified": user.verified,
                "last_login": (
                    datetime.now()
                    if isinstance(user.last_login, type(datetime.now))
                    else user.last_login
                ),
                "is_teacher": user.is_teacher,
                "is_student": user.is_student,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "birth_date": (
                    datetime.now()
                    if isinstance(user.birth_date, type(datetime.now))
                    else user.birth_date
                ),
                "interests": user.interests,
                "skills": user.skills,
                "achievements": user.achievements,
                "courses_completed": user.courses_completed,
                "courses_in_progress": user.courses_in_progress,
            }
            return UserResponse(**user_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The user is not logged in."
        )


@users_router.get("/", summary="Se obtienen todos los usuarios")
async def get_all_users(
    # current_user: User = Depends(require_permission("user:read"))
):
    try:
        result = await UserServices.get_all_users_service()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)


@users_router.get("/{user_id}", summary="Se obtiene un usuario por su ID")
async def get_user_by_id(user_id: str):
    try:
        result = await UserServices.get_user_by_id_service(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)


@users_router.put("/{user_id}", summary="Se actualiza un usuario por su ID")
async def update_user_by_id(user_id: str, payload: UserUpdate):
    try:
        result = await UserServices.update_user_by_id_service(user_id, payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={e})


@users_router.delete("/{user_id}", summary="Se elimina un usuario por su ID")
async def delete_user_by_id(user_id: str):
    try:
        result = await UserServices.delete_user_by_id_service(user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.detail}"
        )
