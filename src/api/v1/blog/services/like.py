from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.db import db_session
from src.api.v1.blog.exceptions import BlogNotFoundException
from src.api.v1.blog.models.blogs import BlogModel
from src.api.v1.blog.models.likes import LikeModel
from src.api.v1.blog.schemas.response import LikeResponse, UserLikedResponse, UserResponse
from src.api.v1.user.models.user import UserModel


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

    async def create(self, user: UserModel, blog_id: UUID) -> LikeResponse:
        """
        Add or remove a like for a blog post by the given user.

        If the blog post exists and the user has already liked it, the like is removed (dislike).
        If the user has not liked the blog post yet, a new like is added.

        Args:
            user (UserModel): The user performing the like or unlike action.
            blog_id (UUID): The unique identifier of the blog post to like or unlike.

        Returns:
            LikeResponse: An object indicating the blog ID and the like status (True if liked, False if unliked).

        Raises:
            BlogNotFoundException: If the blog post with the given ID does not exist.
        """

        blog = await self.session.scalar(
            select(BlogModel).where(BlogModel.id == blog_id)
        )

        if not blog:
            raise BlogNotFoundException

        existing_like = await self.session.scalar(
            select(LikeModel).where(
                LikeModel.user_id == user.id, LikeModel.blog_id == blog_id
            )
        )

        if existing_like:
            await self.session.delete(existing_like)

            return LikeResponse(blog_id=blog_id, like=False)

        like = LikeModel.create(user_id=user.id, blog_id=blog_id)

        self.session.add(like)
        return LikeResponse(blog_id=blog_id, like=True)

    async def get_likes(self, blog_id: UUID) -> UserLikedResponse:
        """
        Retrieve the list of users who liked the specified blog and the total like count.

        Args:
            blog_id (UUID): The unique identifier of the blog.

        Returns:
            UserLikedResponse: The response containing the blog ID, list of users who liked the blog, and the total like count.
        """

        result = await self.session.scalars(
            select(LikeModel)
            .options(joinedload(LikeModel.user))
            .where(LikeModel.blog_id == blog_id)
        )
        likes = result.all()

        users = [UserResponse.model_validate(like.user) for like in likes if like.user]

        return UserLikedResponse(blog_id=blog_id, user=users, total_likes=len(likes))
