from src.api.v1.user.controllers.roles import router as role_router
from src.api.v1.user.controllers.user import router as user_router

__all__ = ["user_router", "role_router"]
