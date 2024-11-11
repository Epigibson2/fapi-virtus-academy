from datetime import datetime
from typing import Optional, List
from beanie import Link
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from models.role_model import Role
from schemas.general_schemas import AutoDates


class UserBase(AutoDates):
    username: str = Field()
    email: EmailStr = Field()
    active: bool = Field(default=True)
    roles: list = Field(default=[])


class UserCreate(AutoDates):
    username: str = Field()
    email: EmailStr = Field()
    password: str = Field()


class UserUpdate(AutoDates):
    username: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=True)
    roles: Optional[list] = Field(default=[])


class UserInDB(UserBase, AutoDates):
    hashed_password: str = Field()


class UserSchema(UserInDB):
    id: Optional[str] = Field(default=None)
    followers: list[str] = Field(default=[])
    following: list[str] = Field(default=[])
    profile_picture: Optional[str] = Field(default="")
    bio: Optional[str] = Field(default="")
    location: Optional[str] = Field(default="")
    website: Optional[str] = Field(default="")
    post_count: int = Field(default=0)
    followers_count: int = Field(default=0)
    following_count: int = Field(default=0)
    private_account: bool = Field(default=False)
    verified: bool = Field(default=False)
    last_login: Optional[datetime] = Field(default=datetime.now)
    is_teacher: bool = Field(default=False)
    is_student: bool = Field(default=False)
    phone_number: Optional[str] = Field(default="")
    gender: Optional[str] = Field(default="")
    birth_date: Optional[datetime] = Field(default=datetime.now)
    interests: Optional[list[str]] = Field(default=[])
    skills: Optional[list[str]] = Field(default=[])
    achievements: Optional[list[str]] = Field(default=[])
    courses_completed: Optional[list[str]] = Field(default=[])
    courses_in_progress: Optional[list[str]] = Field(default=[])

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    active: bool = True
    roles: list[Link[Role]] = []
    created_at: datetime
    updated_at: datetime
    followers: list[str] = []
    following: list[str] = []
    profile_picture: str = ""
    bio: str = ""
    location: str = ""
    website: str = ""
    post_count: int = 0
    followers_count: int = 0
    following_count: int = 0
    private_account: bool = False
    verified: bool = False
    last_login: Optional[datetime] = None
    is_teacher: bool = False
    is_student: bool = False
    phone_number: str = ""
    gender: str = ""
    birth_date: Optional[datetime] = None
    interests: list[str] = []
    skills: list[str] = []
    achievements: list[str] = []
    courses_completed: list[str] = []
    courses_in_progress: list[str] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.isoformat() if dt else None},
    )

    @classmethod
    def from_user(cls, user):
        # Creamos un diccionario base con los campos especiales
        user_dict = {
            "id": str(user.id),
            "roles": [
                str(role.id) if hasattr(role, "id") else str(role)
                for role in user.roles
            ],
        }

        # Agregamos el resto de campos automáticamente
        for field in cls.model_fields.keys():
            if field not in user_dict and hasattr(user, field):
                user_dict[field] = getattr(user, field)

        return cls(**user_dict)
