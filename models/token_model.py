from datetime import datetime
from beanie import Document


class BlacklistToken(Document):
    token: str
    expires_at: datetime
    created_at: datetime = datetime.now()

    class Settings:
        name = "blacklisted_tokens"
        indexes = [
            "token",
            "expires_at",
        ]
