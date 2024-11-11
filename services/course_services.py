from beanie.odm.fields import PydanticObjectId
from models.courses_model import Course
from schemas.course_schema import CourseCreate, CourseUpdate


class CourseServices:

    @staticmethod
    async def create_course(course: CourseCreate) -> Course:
        result = await Course(**course.model_dump())
        await result.insert()
        await result.fetch_all_links()
        return result

    @staticmethod
    async def get_all_courses() -> list[Course]:
        courses = await Course.find_all().to_list()
        for course in courses:
            await course.fetch_all_links()
        return courses

    @staticmethod
    async def get_course_by_id(course_id: PydanticObjectId) -> Course:
        course = await Course.find_one(Course.id == course_id)
        await course.fetch_all_links()
        return course

    @staticmethod
    async def update_course(
        course_id: PydanticObjectId, course: CourseUpdate
    ) -> Course:
        course = await CourseServices.get_course_by_id(course_id)
        await course.update({"set": course.model_dump(exclude_unset=True)})
        await course.fetch_all_links()
        return course

    @staticmethod
    async def delete_course(course_id: PydanticObjectId) -> None:
        course = await CourseServices.get_course_by_id(course_id)
        await course.delete()

    @staticmethod
    async def logic_delete_course(course_id: PydanticObjectId) -> None:
        course = await CourseServices.get_course_by_id(course_id)
        course.status = "deleted"
        await course.save()
