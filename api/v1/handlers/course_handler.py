from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from schemas.course_schema import CourseCreate, CourseResponse, CourseUpdate
from services.course_services import CourseServices


course_router = APIRouter()


@course_router.post("/create-course", response_model=CourseResponse)
async def create_course(course: CourseCreate):
    try:
        result = await CourseServices.create_course(course)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@course_router.get("/get-all-courses", response_model=list[CourseResponse])
async def get_all_courses():
    try:
        return await CourseServices.get_all_courses()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@course_router.get("/get-course-by-id/{course_id}", response_model=CourseResponse)
async def get_course_by_id(course_id: PydanticObjectId):
    try:
        return await CourseServices.get_course_by_id(course_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@course_router.put("/update-course/{course_id}", response_model=CourseResponse)
async def update_course(course_id: PydanticObjectId, course: CourseUpdate):
    try:
        return await CourseServices.update_course(course_id, course)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@course_router.delete("/delete-course/{course_id}")
async def delete_course(course_id: PydanticObjectId):
    try:
        return await CourseServices.delete_course(course_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@course_router.delete("/logic-delete-course/{course_id}")
async def logic_delete_course(course_id: PydanticObjectId):
    try:
        return await CourseServices.logic_delete_course(course_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
