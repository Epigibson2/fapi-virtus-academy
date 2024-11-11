from pydantic import BaseModel
from typing import Optional
import datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class BlacklistTokenSchema(BaseModel):
    token: str
    created_at: datetime.datetime
    expires: datetime.datetime
