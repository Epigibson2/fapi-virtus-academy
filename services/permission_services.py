from click import Argument
from fastapi import HTTPException
from models.permission_model import Permission
from schemas.permission_schema import PermissionCreate, PermissionUpdate
from beanie import PydanticObjectId
from models.role_model import Role
from typing import List


class PermissionsServices:

    @staticmethod
    async def get_all_permissions():
        """Get all permissions

        Returns:
            List of Permission model instances
        """
        permissions = await Permission.find_all().to_list()
        return permissions

    @staticmethod
    async def get_permission_by_id(permission_id: PydanticObjectId):
        """Get a permission by id

        Arguments:
            permission_id: PydanticObjectId = Permission id

        Returns:
            Permission model instance
        """
        permission = await Permission.find_one(Permission.id == permission_id)
        return permission

    @staticmethod
    async def get_permission_by_name(permission_name: str):
        """Get a permission by name
        Arguments:
            permission_name: Permission name

        Returns:
            Permission model instance
        """
        permission = await Permission.find_one(Permission.name == permission_name)
        return permission

    @staticmethod
    async def create_permission(data: PermissionCreate):
        """Create a permission

        Arguments:
            data: PermissionCreate = PermissionCreate model instance

        Returns:
            Permission model instance
        """
        existing_permission = await Permission.find_one(Permission.name == data.name)
        if existing_permission:
            raise HTTPException(status_code=400, detail="Permission already exists")
        new_permission = Permission(**data.model_dump())
        await new_permission.create()
        return new_permission

    @staticmethod
    async def update_permission(
        permission_id: PydanticObjectId, data: PermissionUpdate
    ):
        """Update a permission

        Arguments:
            permission_id: PydanticObjectId = Permission id
            data: PermissionUpdate = PermissionUpdate model instance

        Returns:
            Permission model instance
        """
        permission = await PermissionsServices.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        await permission.update({"$set": data.model_dump(exclude_unset=True)})
        return permission

    @staticmethod
    async def delete_permission(permission_id: PydanticObjectId):
        """Delete a permission

        Arguments:
            permission_id: PydanticObjectId = Permission id

        Returns:
            Dictionary with a message
        """
        permission = await PermissionsServices.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        await permission.delete()
        return {"message": "Permission deleted successfully"}

    @staticmethod
    async def check_permission(user, permission_name: str):
        """Check if a user has a permission

        Arguments:
            user: User model = User model instance
            permission_name: str = Permission name

        Returns:
            Boolean
        """
        # Obtenemos los IDs de los roles del usuario
        role_ids = [role.id for role in user.roles]

        # Cargamos los roles completos
        user_roles = await Role.find({"_id": {"$in": role_ids}}).to_list()

        for role in user_roles:
            # Cargamos los permisos de cada rol
            await role.fetch_link(Role.permissions)
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False

    @staticmethod
    async def get_permissions_by_ids(permission_ids: List[str]):
        """Get permissions by ids

        Arguments:
            permission_ids: List[str] = List of permission ids

        Returns:
            List of Permission model instances
        """
        return await Permission.find(
            {"_id": {"$in": [PydanticObjectId(id) for id in permission_ids]}}
        ).to_list()
