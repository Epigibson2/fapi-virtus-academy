from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from models.comment_model import CommentModel
from models.files_model import File
from models.lesson_model import Lesson
from models.user_model import User
from schemas.general_schemas import AutoDates


class CourseCreate(BaseModel):
    name: str = Field()
    description: str = Field()
    price: float = Field()
    status: str = Field()
    students: list[Link[User]] = Field()
    teacher: Link[User] = Field()
    lessons: list[Link[Lesson]] = Field()
    files: list[Link[File]] = Field()
    certificate: Link[File] = Field()
    duration: int = Field()
    discount: float = Field()
    topics: list[str] = Field()
    level: str = Field()
    rating: float = Field()
    comments: list[Link[CommentModel]] = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Course Name",
                "description": "Course Description",
                "price": 100.0,
                "status": "active",
                "students": ["user_id"],
                "teacher": "user_id",
                "lessons": ["lesson_id"],
                "files": ["file_id"],
                "certificate": "file_id",
                "duration": 10,
                "discount": 0.0,
                "topics": ["topic_id"],
                "level": "beginner",
                "rating": 4.5,
                "comments": ["comment_id"],
            }
        }
    }


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    status: Optional[str] = Field(default=None)
    students: Optional[list[Link[User]]] = Field(default=None)
    teacher: Optional[Link[User]] = Field(default=None)
    lessons: Optional[list[Link[Lesson]]] = Field(default=None)
    files: Optional[list[Link[File]]] = Field(default=None)
    certificate: Optional[Link[File]] = Field(default=None)
    duration: Optional[int] = Field(default=None)
    discount: Optional[float] = Field(default=None)
    topics: Optional[list[str]] = Field(default=None)
    level: Optional[str] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    comments: Optional[list[Link[CommentModel]]] = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Course Name",
                "description": "Course Description",
                "price": 100.0,
                "status": "active",
                "students": ["user_id"],
                "teacher": "user_id",
                "lessons": ["lesson_id"],
                "files": ["file_id"],
                "certificate": "file_id",
                "duration": 10,
                "discount": 0.0,
                "topics": ["topic_id"],
                "level": "beginner",
                "rating": 4.5,
                "comments": ["comment_id"],
            }
        }
    }


class CourseResponse(AutoDates):
    id: str = Field()
    name: str = Field()
    description: str = Field()
    price: float = Field()
    status: str = Field()
    students: list[Link[User]] = Field()
    teacher: Link[User] = Field()
    lessons: list[Link[Lesson]] = Field()
    files: list[Link[File]] = Field()
    certificate: Link[File] = Field()
    duration: int = Field()
    discount: float = Field()
    topics: list[str] = Field()
    level: str = Field()
    rating: float = Field()
    comments: list[Link[CommentModel]] = Field()
