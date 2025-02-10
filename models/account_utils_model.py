from datetime import datetime
from beanie import Document, Link
from pydantic import Field, EmailStr
from models.user_model import User
from schemas.file_schemas import FileBase


class ResetPassword(Document):
    old_password: str = Field()
    new_password: str = Field()
    email: str = Field()


    class Settings:
        name = "reset_password"
        use_state_management = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "text/plain",
                "new_password": "text/plain",
                "email": "text/plain",
            }
        }
    }