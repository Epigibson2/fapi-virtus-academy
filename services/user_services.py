from datetime import datetime, timedelta
from typing import Optional
import logging

from fastapi import HTTPException, status

from models.role_model import Role
from models.user_model import User
from models.token_model import BlacklistToken
from schemas.permission_schema import PermissionCreate
from schemas.role_schemas import RoleCreate
from schemas.user_schema import UserCreate, UserUpdate, UserInDB
from schemas.auth_schema import TokenSchema
from services.util_services import get_valid_document, user_exists
from utils.auth_utils import get_password_hash, verify_password
from services.role_services import RoleService
from services.permission_services import PermissionsServices

logger = logging.getLogger(__name__)


class UserServices:

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        try:
            user = await UserServices.get_user_by_email_service(email=email)
            if not user:
                logger.warning(f"No user found with email: {email}")
                return None

            if not user.hashed_password:
                logger.error(f"User {email} has no hashed password stored")
                return None

            # Verificar que el hash esté en formato correcto
            if not user.hashed_password.startswith(
                "$2b$"
            ) and not user.hashed_password.startswith("$2a$"):
                logger.error(f"Invalid hash format for user {email}")
                return None

            is_valid = verify_password(
                plain_password=password, hashed_password=user.hashed_password
            )

            if not is_valid:
                logger.warning(f"Invalid password attempt for user: {email}")
                return None

            return user

        except Exception as e:
            logger.error(f"Authentication error for {email}: {str(e)}")
            return None

    @staticmethod
    async def logout_service(data: TokenSchema):
        """Invalidar tokens al hacer logout

        Arguments:
            access_token: str = Token de acceso actual
            refresh_token: str = Token de refresh (opcional)

        Returns:
            dict = Mensaje de confirmación
        """
        try:
            token_doc = BlacklistToken(
                token=data.access_token, expires_at=datetime.now() + timedelta(days=1)
            )
            await token_doc.create()

            if data.refresh_token:
                refresh_token_doc = BlacklistToken(
                    token=data.refresh_token,
                    expires_at=datetime.now() + timedelta(days=7),
                )
                await refresh_token_doc.create()

            return {"message": "Logout exitoso"}

        except Exception as e:
            logger.error(f"Error durante el logout: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al procesar el logout",
            )

    @staticmethod
    async def create_user_service(user: UserCreate):
        """Create a user

        Arguments:
            user: UserCreate = UserCreate model instance

        Returns:
            User model instance
        """
        try:
            # Check if username already exists
            await user_exists(user.username, user.email)

            # Hash password
            hashed_password = get_password_hash(user.password)
            role_created = None

            admin_permissions = ["crear", "editar", "lectura", "eliminar"]
            permissions_created = []
            for permission in admin_permissions:
                try:
                    permission_data = PermissionCreate(
                        name=permission,
                        description=f"Permiso para {permission}",
                    )
                    permission_result = await PermissionsServices.create_permission(permission_data)
                    if permission_result:
                        permissions_created.append(str(permission_result.name))
                except Exception as e:
                    # Si el permiso ya existe, lo recuperamos (evita detener el flujo)
                    existing_permission = await PermissionsServices.get_permission_by_name(permission)
                    if existing_permission:
                        permissions_created.append(existing_permission.name)


            if user.is_admin:
                admin_role = None
                try:
                    search_if_role_already_exist = await RoleService.get_role_by_name("Administrador")
                    if search_if_role_already_exist:
                        admin_role = search_if_role_already_exist
                    else:
                        admin_role = RoleCreate(
                            name=f"Administrador",
                            description=f"Permiso para {user.username}",
                            permissions=permissions_created,
                        )
                        role_created = await RoleService.create_role(name=admin_role.name, description=admin_role.description, permissions=admin_role.permissions)

                except Exception as e:
                    if e.args[0] == 400:
                        existing_role = await RoleService.get_role_by_name(admin_role.name)
                        if existing_role:
                            role_created = existing_role
            else:
                user_role = RoleCreate(
                    name=f"User",
                    description=f"Permiso para usuarios",
                    permissions=permissions_created,
                )
                try:
                    result = await RoleService.create_role(user_role.name, description=user_role.description, permissions=user_role.permissions)
                    role_created = result

                except Exception as e:
                    print("Error creating role: " + str(e))
                    search_role = await Role.find_one(Role.name == user_role.name)
                    if search_role:
                        role_created = search_role

            user_in_db = UserInDB(
                username=user.username,
                email=user.email,
                hashed_password=hashed_password,
                active=True,
                roles=[role_created.id],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            new_user = User(**user_in_db.model_dump())
            await new_user.create()
            return new_user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ocurrió un error al crear el usuario: {str(e)}",
            )

    @staticmethod
    async def get_all_users_service():
        """Get all users

        Returns:
            List of User model instances
        """
        users = await User.find_all().to_list()
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
            )
        return users

    @staticmethod
    async def get_user_by_id_service(user_id: str):
        """Get a user by id

        Arguments:
            user_id: str = User id

        Returns:
            User model instance
        """
        user = await get_valid_document(user_id, User)
        return user

    @staticmethod
    async def get_user_by_username_service(username: str):
        """Get a user by username

        Arguments:
            username: str = Username

        Returns:
            User model instance
        """
        user = await User.find_one(User.username == username)
        return user

    @staticmethod
    async def get_user_by_email_service(email: str):
        """Get a user by email

        Arguments:
            email: str = Email

        Returns:
            User model instance
        """
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def update_user_by_id_service(user_id: str, data: UserUpdate):
        """Update a user by id

        Arguments:
            user_id: str = User id
            data: UserUpdate = UserUpdate model instance

        Returns:
            User model instance
        """
        user = await get_valid_document(user_id, User)
        await user.update({"$set": data.model_dump(exclude_unset=True)})
        return user

    @staticmethod
    async def delete_user_by_id_service(user_id: str):
        """Delete a user by id

        Arguments:
            user_id: str = User id

        Returns:
            Dictionary with a message
        """
        user = await get_valid_document(user_id, User)
        await user.delete()
        return {"message": "User deleted successfully"}
