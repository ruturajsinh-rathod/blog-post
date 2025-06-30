from apps.v1.blog.models.blogs import BlogModel
from apps.v1.user.models.roles import RoleModel
from apps.v1.user.models.user import UserModel
from core.db import Base

__all__ = ["Base", "BlogModel", "RoleModel", "UserModel"]
