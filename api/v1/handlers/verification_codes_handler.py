from fastapi import APIRouter, HTTPException, status
from services.verification_codes_services import VerificationCodeService

verification_codes_router = APIRouter()


@verification_codes_router.post("/")
async def create_verification(user_id: str):
    try:
        return await VerificationCodeService.create_verification_code(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )

@verification_codes_router.get("/")
async def get_verification_code(code: str, user_id: str):
    try:
        return await VerificationCodeService.get_verification_code(code, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )

@verification_codes_router.post("/validate-verification-code")
async def validate_verification_code(code:str, user_id: str):
    try:
        return await VerificationCodeService.validate_verification_code(code, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )