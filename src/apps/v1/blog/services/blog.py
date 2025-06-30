from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.constants as constants
from src.apps.v1.blog.exceptions import BlogNotFoundException, DuplicateBlogException
from src.apps.v1.blog.models.blogs import BlogModel
from src.apps.v1.user.models.user import UserModel
from database.db import db_session


class BlogService:
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

    async def create_blog(self, name: str, content: str, user: UserModel) -> BlogModel:
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
            select(BlogModel).where(BlogModel.name == name)
        )

        if blog:
            raise DuplicateBlogException

        blog = BlogModel.create(name=name, content=content, author_id=user.id)
        self.session.add(blog)

        return blog

    async def get_all(self, params: Params) -> Page[BlogModel]:
        """
        Retrieve a paginated list of all blog posts.

        Args:
            params (Params): Pagination parameters provided by FastAPI pagination.

        Returns:
            Page[BlogModel]: A paginated list of blog posts.
        """
        stmt = select(BlogModel).where(BlogModel.deleted_at.is_(None))
        return await paginate(self.session, stmt, params)

    async def get_by_id(self, blog_id: UUID) -> BlogModel:
        """
        Retrieve a blog post by its unique identifier.

        Args:
            blog_id (UUID): The unique identifier of the blog post.

        Raises:
            BlogNotFoundException: If no blog with the given ID exists.

        Returns:
            BlogModel: The blog post instance.
        """

        blog = await self.session.scalar(
            select(BlogModel).where(
                BlogModel.id == blog_id, BlogModel.deleted_at.is_(None)
            )
        )

        if not blog:
            raise BlogNotFoundException

        return blog

    async def delete_by_id(self, blog_id: UUID) -> dict[str, str]:
        """
        Delete a blog post by its unique identifier.

        Args:
            blog_id (UUID): The unique identifier of the blog post to be deleted.

        Raises:
            BlogNotFoundException: If no blog with the given ID exists.

        Returns:
            dict[str, str]: A success message indicating deletion.
        """

        blog = await self.session.scalar(
            select(BlogModel).where(
                BlogModel.id == blog_id, BlogModel.deleted_at.is_(None)
            )
        )

        if not blog:
            raise BlogNotFoundException

        blog.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)

        return {"message": constants.BLOG_DELETE_SUCCESS}
