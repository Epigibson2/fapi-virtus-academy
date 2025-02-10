from fastapi import HTTPException, status

from models.account_utils_model import ResetPassword
from services.user_services import UserServices
from utils.auth_utils import verify_password, get_password_hash


class AccountUtilsServices:

    @staticmethod
    async def reset_password(data: ResetPassword):
        user = await UserServices.get_user_by_email_service(email=data.email)
        is_valid = verify_password(
            plain_password=data.old_password, hashed_password=user.hashed_password
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al intentar cambiar la contraseña: La contraseña actual no es correcta.",
            )
        new_password = get_password_hash(data.new_password)
        user.hashed_password = new_password
        await user.save()
        return user
