from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from schemas.permission_schema import PermissionCreate, PermissionUpdate
from services.permission_services import PermissionsServices


permission_router = APIRouter()


@permission_router.post("/")
async def create_permission_handler(data: PermissionCreate):
    try:
        return await PermissionsServices.create_permission(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
    
@permission_router.get("/")
async def get_all_permissions_handler():
    try:
        return await PermissionsServices.get_all_permissions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
    
@permission_router.get("/{permission_id}")
async def get_permission_by_id_handler(permission_id: str):
    try:
        return await PermissionsServices.get_permission_by_id(permission_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
    

@permission_router.put("/{permission_id}")
async def update_permission_handler(permission_id: PydanticObjectId, data: PermissionUpdate):
    try:
        return await PermissionsServices.update_permission(permission_id, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
    
@permission_router.delete("/{permission_id}")
async def delete_permission_handler(permission_id: str):
    try:
        return await PermissionsServices.delete_permission(permission_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )
