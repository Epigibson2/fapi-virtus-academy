from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from models.role_model import Role
from models.user_model import User
from schemas.role_schemas import RoleUpdate
from services.permission_services import PermissionsServices
from services.role_services import RoleService
from services.user_services import UserServices
from utils.permission_utils import require_permission
from typing import List

role_router = APIRouter()


@role_router.post("/")
async def create_new_role(
    name: str,
    description: str,
    permissions: List[str],
    current_user: User = Depends(require_permission(["manage_roles", "crear"])),
):
    try:
        return await RoleService.create_role(name, description, permissions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.get("/")
async def get_all_roles_handler(
    current_user: User = Depends(require_permission(["manage_roles", "lectura"]))
):
    try:
        roles = await RoleService.get_all_roles()
        return roles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.get("/{role_id}")
async def get_role_by_id_handler(
    role_id: PydanticObjectId,
    current_user: User = Depends(require_permission(["manage_roles", "lectura"])),
):
    try:
        return await RoleService.get_role_by_id(role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.put("/{role_id}")
async def update_role_handler(
    role_id: PydanticObjectId,
    data: RoleUpdate,
    current_user: User = Depends(require_permission(["manage_roles", "editar"])),
):
    try:
        return await RoleService.update_role(role_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.post("/users/{user_id}/roles")
async def assign_role_handler(
    user_id: str,
    role_name: str,
    current_user: User = Depends(require_permission(["manage_roles", "crear"])),
):
    try:
        user = await UserServices.get_user_by_id_service(user_id)
        return await RoleService.assign_role_to_user(user, role_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
