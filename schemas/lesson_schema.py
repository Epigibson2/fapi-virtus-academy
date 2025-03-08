from pydantic import BaseModel, Field
from models.comment_model import CommentModel
from models.files_model import File
from beanie import Link
from typing import Optional
from datetime import datetime
from beanie.odm.fields import PydanticObjectId


class LessonCreate(BaseModel):
    name: str = Field()
    course_from: PydanticObjectId = Field()
    description: str = Field()
    video_url: str = Field()
    duration: int = Field()
    files: Optional[list[Link[File]]] = Field([])
    comments: Optional[list[Link[CommentModel]]] = Field([])

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Course Name",
                "description": "Course Description",
                "video_url": "URL_ADDRESS.com/video.mp4",
                "duration": 120,
                "files": [],
                "comments": [],
                "created_at": "2023-09-14T12:00:00",
                "updated_at": "2023-09-14T12:00:00",
            }
        }
    }


class LessonUpdate(BaseModel):
    name: Optional[str] = Field()
    description: Optional[str] = Field()
    course_from: PydanticObjectId = Field()
    video_url: Optional[str] = Field()
    duration: Optional[int] = Field()
    files: Optional[list[Link[File]]] = Field()
    comments: Optional[list[Link[CommentModel]]] = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Course Name",
                "description": "Course Description",
                "video_url": "URL_ADDRESS.com/video.mp4",
                "duration": 120,
                "files": [],
                "comments": [],
            }
        }
    }


class LessonUpdate(BaseModel):
    id: str = Field()
    name: str = Field()
    description: str = Field()
    video_url: str = Field()
    duration: int = Field()
    files: list[Link[File]] = Field()
    comments: list[Link[CommentModel]] = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
