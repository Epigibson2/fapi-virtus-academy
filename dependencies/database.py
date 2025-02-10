from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
from models.account_utils_model import ResetPassword
from models.role_model import Permission, Role
from models.user_model import User
from models.files_model import File
from models.courses_model import Course
from models.token_model import BlacklistToken
from models.verification_code_model import VerificationCode


async def init_db():
    """
    Inicializa la conexión a la base de datos y configura los modelos de documentos.

    :return: None
    """
    client = AsyncIOMotorClient(settings.DATABASE_URL)

    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            Permission,
            Role,
            File,
            Course,
            BlacklistToken,
            ResetPassword,
            VerificationCode
        ],
    )
