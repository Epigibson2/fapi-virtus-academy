from beanie import Document, Link
from pydantic import Field
from schemas.user_schema import UserSchema
from models.role_model import Role


class User(Document, UserSchema):
    """Override fields from Schema."""

    roles: list[Link[Role]] = []
    initial_prompt: bool = Field(default=False)

    class Settings:
        name = "users"
