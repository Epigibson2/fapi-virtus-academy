from beanie import PydanticObjectId
from fastapi import HTTPException
from models.role_model import Role, Permission
from typing import List
from schemas.role_schemas import RoleUpdate


class RoleService:

    @staticmethod
    async def create_role(name: str, description: str, permissions: List[str]):
        """Create a role

        Arguments:
            name: string = Role name
            description: string = Role description
            permissions: List[str] = List of permission names
        """
        existing_role = await Role.find_one(Role.name == name)
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already exists")

        permission_objects = []
        for perm_name in permissions:
            perm = await Permission.find_one(Permission.name == perm_name)
            if not perm:
                raise HTTPException(
                    status_code=400, detail=f"Permission {perm_name} does not exist"
                )
            permission_objects.append(perm)

        new_role = Role(
            name=name, description=description, permissions=permission_objects
        )
        await new_role.create()
        return new_role

    @staticmethod
    async def get_role_by_id(role_id: PydanticObjectId):
        """Get a role by id

        Arguments:
            role_id: string = Role id

        Returns:
            Role model instance
        """
        role = await Role.find_one(Role.id == role_id)
        await role.fetch_link(Role.permissions)
        return role

    @staticmethod
    async def get_role_by_name(name: str):
        """Get a role by name

        Arguments:
            name: string = Role name

        Returns:
            Role model instance
        """
        role = await Role.find_one(Role.name == name)
        await role.fetch_link(Role.permissions)
        return role

    @staticmethod
    async def get_all_roles():
        """Get all roles

        Returns:
            List of Role model instances
        """
        roles = await Role.find_all().to_list()
        for role in roles:
            await role.fetch_all_links()
        return roles

    @staticmethod
    async def update_role(role_id: PydanticObjectId, data: RoleUpdate):
        """Update a role

        Arguments:
            role_id: string = Role id
            data: RoleUpdate = RoleUpdate model instance

        Returns:
            Role model instance
        """
        role = await RoleService.get_role_by_id(role_id)
        await role.update({"$set": data.model_dump(exclude_unset=True)})
        new_role = await RoleService.get_role_by_id(role_id)
        return new_role

    @staticmethod
    async def delete_role(role_id: PydanticObjectId):
        """Delete a role

        Arguments:
            role_id: string = Role id

        Returns:
            Boolean
        """
        role = await RoleService.get_role_by_id(role_id)
        result = await role.delete()
        return result

    @staticmethod
    async def assign_role_to_user(user, role_name: str):
        """Assign a role to a user

        Arguments:
            user: User model = User model instance
            role_name: string = Role name

        Raises:
            HTTPException: If role not found

        Returns:
            User model
        """
        role = await Role.find_one(Role.name == role_name)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        if role not in user.roles:
            user.roles.append(role)
            await user.save()
        return user
