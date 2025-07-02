from src.api.v1.blog.controllers.blog import router as blog_router
from src.api.v1.blog.controllers.comment import router as comment_router

__all__ = ["blog_router", "comment_router"]
