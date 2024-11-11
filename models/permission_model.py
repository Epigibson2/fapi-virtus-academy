from beanie import Document
from pydantic import Field


class Permission(Document):
    name: str = Field(...)
    description: str = Field(...)

    class Settings:
        name = "permissions"