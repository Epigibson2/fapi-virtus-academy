from fastapi import APIRouter, HTTPException, status

from models.account_utils_model import ResetPassword
from services.account_utils_services import AccountUtilsServices

account_utils_router = APIRouter()


@account_utils_router.post('/reset-password', summary='Reset password', tags=['Account Utils'])
async def reset_password(data: ResetPassword):
    try:
        result = await AccountUtilsServices.reset_password(data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )