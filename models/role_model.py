from beanie import Document, Link
from typing import List
from pydantic import Field
from models.permission_model import Permission

class Role(Document):
    name: str = Field(...)
    description: str = Field(...)
    permissions: List[Link[Permission]] = Field(default_factory=list)

    class Settings:
        name = "roles"

