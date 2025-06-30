from fastapi import APIRouter

from src.apps.v1.auth.controllers import auth_router
from src.apps.v1.blog.controllers import blog_router, like_router
from src.apps.v1.user.controllers import role_router, user_router

router = APIRouter(prefix="/api/v1")

# Attach child routers to main router
router.include_router(auth_router)
router.include_router(blog_router)
router.include_router(user_router)
router.include_router(role_router)
router.include_router(like_router)

__all__ = ["router"]
