from datetime import datetime
from beanie import Document, Link
from pydantic import Field
from models.user_model import User
from schemas.file_schemas import FileBase


class File(Document):
    name: str = Field()
    path: str = Field()
    type: str = Field()
    owner: Link[User] = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "files"
        use_state_management = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "file",
                "path": "/files/file.txt",
                "type": "text/plain",
                "owner": "user_id",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
            }
        }
    }
