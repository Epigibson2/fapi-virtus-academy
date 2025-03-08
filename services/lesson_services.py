from fastapi import HTTPException, status
from models.lesson_model import Lesson
from schemas.lesson_schema import LessonCreate, LessonUpdate
from beanie.odm.fields import PydanticObjectId


class LessonServices:

    @staticmethod
    async def get_all_lessons():
        try:
            lesson = await Lesson.find_all().to_list()
            return lesson
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")

    @staticmethod
    async def get_lesson_by_id(lesson_id: PydanticObjectId):
        try:
            lesson = await Lesson.find_one(Lesson.id == lesson_id)
            return lesson
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")

    @staticmethod
    async def create_lesson(lesson: LessonCreate):
        try:
            lesson = await Lesson(**lesson.dict()).create()
            return lesson
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create lesson: {e}")

    @staticmethod
    async def delete_lesson(lesson_id: PydanticObjectId):
        try:
            lesson = await LessonServices.get_lesson_by_id(lesson_id)
            await lesson.delete()
            return {"message": "Lesson deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")

    @staticmethod
    async def update_lesson(lesson_id: PydanticObjectId, lesson: LessonUpdate):
        try:
            lesson = await LessonServices.get_lesson_by_id(lesson_id)
            try:
                await lesson.update({"set": lesson.model_dump(exclude_unset=True)})
                await lesson.fetch_all_links()
                return lesson
            except Exception as e:
                raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update lesson: {e}")
