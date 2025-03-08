from datetime import datetime

from beanie import Document, Link
from pydantic import Field

from models.comment_model import CommentModel
from models.files_model import File

from typing import Optional
from beanie.odm.fields import PydanticObjectId


class Lesson(Document):
    name: str = Field()
    course_from: PydanticObjectId = Field()
    description: str = Field()
    video_url: str = Field()
    duration: int = Field()
    files: Optional[list[Link[File]]] = Field([])
    comments: Optional[list[Link[CommentModel]]] = Field([])
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    class Settings:
        name = "lessons"
        use_state_management = True
