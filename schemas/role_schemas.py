from pydantic import BaseModel
from typing import List, Optional
from schemas.general_schemas import AutoDates


class RoleCreate(AutoDates):
    name: str
    description: str
    permissions: List[str]


class RoleUpdate(AutoDates):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
