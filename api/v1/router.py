from fastapi import APIRouter
from api.v1.handlers import (
    user_handler,
    role_handler,
    permission_handler,
    file_handler,
    course_handler,
    stripe_handler,
    health_check_handler
)
from api.auth.jwt import auth_router

router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_handler.users_router, prefix="/user", tags=["Users"])
router.include_router(role_handler.role_router, prefix="/role", tags=["Roles"])
router.include_router(
    permission_handler.permission_router, prefix="/permission", tags=["Permissions"]
)
router.include_router(file_handler.file_router, prefix="/file", tags=["Files"])
router.include_router(course_handler.course_router, prefix="/course", tags=["Courses"])
router.include_router(health_check_handler.health_check_router, prefix="/health-check",
                      tags=["Health Check"]),
router.include_router(stripe_handler.stripe_router, prefix="/stripe", tags=["Stripe"])
