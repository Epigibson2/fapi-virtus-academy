from datetime import datetime

from beanie import Document
from pydantic import Field


class VerificationCode(Document):
    code: str
    origin: str
    owner: str
    expiration: datetime
    status: bool
    created_at: datetime = Field()

    class Settings:
        name = "verification_codes"
        use_state_management = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "code": "23455342",
                "origin": "reset_password",
                "owner": "text/plain",
                "expiration": "2021-01-01T00:00:00",
                "status": "true",
                "created_at": "2021-01-01T00:00:00",
            }
        }
    }