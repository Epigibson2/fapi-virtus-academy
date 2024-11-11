from datetime import datetime

from beanie import Document, Link
from pydantic import Field

from models.comment_model import CommentModel
from models.files_model import File


class Lesson(Document):
    name: str = Field()
    description: str = Field()
    video_url: str = Field()
    duration: int = Field()
    files: list[Link[File]] = Field()
    comments: list[Link[CommentModel]] = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "lessons"
        use_state_management = True
