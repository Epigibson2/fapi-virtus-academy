from datetime import datetime

from beanie import Document
from pydantic import Field


class CommentModel(Document):
    content: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "comments"
        use_state_management = True
