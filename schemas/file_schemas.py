from typing import Optional
from beanie import Link
from pydantic import BaseModel, Field
from models.user_model import User
from schemas.general_schemas import AutoDates


class FileBase(AutoDates):
    name: str = Field()
    path: str = Field()
    type: str = Field()
    is_deleted: bool = Field(default=False)
    owner: Link[User] = Field()


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    name: Optional[str] = Field(default=None)
    path: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    is_deleted: Optional[bool] = Field(default=None)
    owner: Optional[Link[User]] = Field(default=None)


class FileInDb(FileBase):
    id: Optional[str] = Field(default=None)


class FileResponse(FileInDb):
    model_config = {
        "from_attributes": True,
    }
