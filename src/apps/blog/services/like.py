from datetime import datetime, timezone
from typing import Annotated, Any, Coroutine
from uuid import UUID

from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import constants
from apps.blog.exceptions import BlogNotFoundException, DuplicateBlogException
from apps.blog.models.blogs import BlogModel
from apps.blog.models.likes import LikeModel
from apps.user.models.user import UserModel
from core.db import db_session


class LikeService:
    """
    Service class for managing blog-related database operations.

    Attributes:
        session (AsyncSession): Asynchronous SQLAlchemy session injected via dependency.
    """

    def __init__(self, session: Annotated[AsyncSession, Depends(db_session)]) -> None:
        """
        Initialize BlogService with an asynchronous database session.

        Args:
            session (AsyncSession): An asynchronous database session provided by dependency injection.
        """

        self.session = session

    async def create(self, user: UserModel, blog_id:UUID) -> dict[str, str]:
        """
        Create a new blog post in the database.

        Checks if a blog with the same name already exists. If found, raises a DuplicateBlogException.

        Args:
            name (str): The unique name or title for the blog post.
            content (str): The content or body of the blog post.
            user (UserModel): The user creating the blog post.

        Raises:
            DuplicateBlogException: If a blog with the same name already exists.

        Returns:
            BlogModel: The newly created blog post instance.
        """

        blog = await self.session.scalar(
            select(BlogModel).where(BlogModel.id == blog_id)
        )

        if not blog:
            raise BlogNotFoundException

        like = LikeModel.create(user_id=user.id, blog_id=blog_id)

        # user.likes.append(like)
        self.session.add(like)
        return {"message": constants.BLOG_LIKE_SUCCESS}
