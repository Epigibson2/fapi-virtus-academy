from fastapi import APIRouter, HTTPException, status
from services.lesson_services import LessonServices
from schemas.lesson_schema import LessonCreate, LessonUpdate
from beanie import PydanticObjectId


lesson_router = APIRouter()


@lesson_router.get("/{lesson_id}", summary="Get a lesson by id", tags=["Lesson"])
async def get_lesson_by_id(lesson_id: PydanticObjectId):
    try:
        lesson = await LessonServices.get_lesson_by_id(lesson_id)
        return lesson
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")


@lesson_router.get("/", summary="Get all lessons", tags=["Lesson"])
async def get_all_lessons():
    try:
        lesson = await LessonServices.get_all_lessons()
        return lesson
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")


@lesson_router.post("/", summary="Create a lesson", tags=["Lesson"])
async def create_lesson(lesson: LessonCreate):
    try:
        lesson = await LessonServices.create_lesson(lesson)
        return lesson
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create lesson: {e}")


@lesson_router.put("/{lesson_id}", summary="Update a lesson", tags=["Lesson"])
async def update_lesson(lesson_id: PydanticObjectId, lesson: LessonUpdate):
    try:
        lesson = await LessonServices.update_lesson(lesson_id, lesson)
        return lesson
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")


@lesson_router.delete("/{lesson_id}", summary="Delete a lesson", tags=["Lesson"])
async def delete_lesson(lesson_id: PydanticObjectId):
    try:
        lesson = await LessonServices.delete_lesson(lesson_id)
        return lesson
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {e}")
