
from typing import Optional
from pydantic import Field
from schemas.general_schemas import AutoDates


class PermissionBase(AutoDates):
    name: str = Field()
    description: str = Field()

class PermissionCreate(PermissionBase, AutoDates, extra="forbid"):
    pass

class PermissionUpdate(PermissionBase, AutoDates, extra="forbid"):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
