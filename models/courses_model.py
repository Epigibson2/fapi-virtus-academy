from datetime import datetime
from beanie import Document, Link
from pydantic import Field

from models.files_model import File
from models.lesson_model import Lesson
from models.user_model import User
from models.comment_model import CommentModel


class Course(Document):
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
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "courses"
        use_state_management = True

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
