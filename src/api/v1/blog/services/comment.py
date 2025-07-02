from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.db import db_session
from src import constants
from src.api.v1.blog.exceptions import (
    BlogNotFoundException,
    CommentNotFoundException,
    InvalidCredsException,
    InvalidParentCommentBlogException,
    InvalidParentCommentNestingException,
    ParentCommentNotFoundException,
)
from src.api.v1.blog.models import BlogModel, CommentLikeModel, CommentModel
from src.api.v1.blog.schemas.response import CommentLikeResponse
from src.api.v1.user.enums import RoleEnum
from src.api.v1.user.models import UserModel


class CommentService:
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

    async def create_comment(
        self,
        content: str,
        blog_id: UUID,
        user: UserModel,
        parent_comment_id: UUID | None = None,
    ) -> CommentModel:
        """
        Create a new comment on a blog or as a reply to another comment.

        Args:
            content (str): The text content of the comment.
            blog_id (UUID): The blog being commented on.
            user (UserModel): The user creating the comment.
            parent_comment_id (UUID | None): Optional ID of the parent comment for nested replies.

        Returns:
            CommentModel: The newly created comment instance.
        """

        blog = await self.session.scalar(
            select(BlogModel).where(
                BlogModel.id == blog_id, BlogModel.deleted_at.is_(None)
            )
        )

        if not blog:
            raise BlogNotFoundException

        if parent_comment_id:
            parent_comment = await self.session.scalar(
                select(CommentModel).where(CommentModel.id == parent_comment_id)
            )
            if parent_comment.parent_comment_id:
                raise InvalidParentCommentNestingException
            if not parent_comment:
                raise ParentCommentNotFoundException
            if parent_comment.blog_id != blog_id:
                raise InvalidParentCommentBlogException

        comment = CommentModel.create(
            content=content,
            author_id=user.id,
            blog_id=blog_id,
            parent_comment_id=parent_comment_id,
        )

        self.session.add(comment)
        return comment

    async def get_parent_comments(self, blog_id: UUID) -> BlogModel:
        """
        Retrieve a blog along with its top-level (parent) comments.

        Args:
            blog_id (UUID): The unique identifier of the blog.

        Returns:
            BlogModel: The blog instance including its parent comments.

        Raises:
            BlogNotFoundException: If the blog with the given ID does not exist or is deleted.
        """
        blog = await self.session.scalar(
            select(BlogModel)
            .options(joinedload(BlogModel.comments))
            .where(BlogModel.id == blog_id, BlogModel.deleted_at.is_(None))
        )

        if not blog:
            raise BlogNotFoundException

        return blog

    async def get_replies(self, comment_id: UUID) -> Sequence[CommentModel]:
        """
        Retrieve all replies for a given comment.

        Args:
            comment_id (UUID): The unique identifier of the parent comment.

        Returns:
            Sequence[CommentModel]: A list of replies to the specified comment.
        """

        comments = await self.session.scalars(
            select(CommentModel).where(CommentModel.parent_comment_id == comment_id)
        )

        return comments.all()

    async def like_or_unlike_comment(
        self, comment_id: UUID, user: UserModel
    ) -> CommentLikeResponse:
        """
        Toggle like status for a comment.

        If the user has already liked the comment, the like will be removed (unlike).
        Otherwise, a new like will be added.

        Args:
            comment_id (UUID): The unique identifier of the comment.
            user (UserModel): The currently authenticated user.

        Returns:
            CommentLikeResponse: The updated like status of the comment.
        """

        existing_like = await self.session.scalar(
            select(CommentLikeModel).where(
                CommentLikeModel.user_id == user.id,
                CommentLikeModel.comment_id == comment_id,
            )
        )

        if existing_like:
            await self.session.delete(existing_like)

            return CommentLikeResponse(comment_id=comment_id, like=False)

        like = CommentLikeModel.create(user_id=user.id, comment_id=comment_id)

        self.session.add(like)
        return CommentLikeResponse(comment_id=comment_id, like=True)

    async def remove_comment(self, user: UserModel, comment_id: UUID) -> dict[str, str]:
        """
        Delete a comment if the user is authorized.

        Only the comment's author or an admin can delete the comment.

        Args:
            user (UserModel): The currently authenticated user.
            comment_id (UUID): The unique identifier of the comment to delete.

        Returns:
            dict[str, str]: A confirmation message upon successful deletion.

        Raises:
            CommentNotFoundException: If the comment does not exist.
            InvalidCredsException: If the user is not authorized to delete the comment.
        """
        comment = await self.session.scalar(
            select(CommentModel).where(CommentModel.id == comment_id)
        )

        if not comment:
            raise CommentNotFoundException

        if user.role.name != RoleEnum.ADMIN and comment.author_id != user.id:
            raise InvalidCredsException

        await self.session.delete(comment)
        return {"message": constants.COMMENT_DELETED_SUCCESSFULLY}
