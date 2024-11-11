from fastapi import HTTPException, Depends
from api.deps.user_deps import get_current_user
from models.user_model import User
from services.permission_services import PermissionsServices


def require_permission(list_permissions: list[str]):
    async def wrapper(current_user: User = Depends(get_current_user)):
        for permission in list_permissions:
            if not await PermissionsServices.check_permission(current_user, permission):
                raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user

    return wrapper
