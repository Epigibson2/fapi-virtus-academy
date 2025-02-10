import datetime
import random

from models.account_utils_model import ResetPassword
from models.verification_code_model import VerificationCode
from services.account_utils_services import AccountUtilsServices


class VerificationCodeService:

    @staticmethod
    async def create_verification_code(user_id: str):
        random_code = str(random.randint(100000, 999999))
        new_code = VerificationCode(
            code=random_code,
            origin="reset_password",
            owner=user_id,
            status=True,
            expiration=datetime.datetime.today() + datetime.timedelta(minutes=5),
            created_at=datetime.datetime.today()
        )
        code_created = await new_code.insert()
        return code_created

    @staticmethod
    async def get_verification_code(code: str, user_id: str):
        result = await VerificationCode.find_one({"code": code, "owner": user_id})
        return result


    @staticmethod
    async def validate_verification_code(code: str, user_id: str):
        get_code_to_validate = await VerificationCodeService.get_verification_code(code, user_id)
        if not get_code_to_validate.status:
            raise Exception("The verification code has been used.")
        if get_code_to_validate.expiration < datetime.datetime.today():
            get_code_to_validate.status = False
            await get_code_to_validate.save()
            raise Exception(f"The code {code} has expired, try to generate a new one.")
        else:
            get_code_to_validate.status = False
            await get_code_to_validate.save()
        return get_code_to_validate


