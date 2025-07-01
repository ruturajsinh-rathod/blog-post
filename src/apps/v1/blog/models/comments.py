import uuid
from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from src.core.utils.mixins import TimeStampMixin


class CommentModel(Base, TimeStampMixin):
    """
    SQLAlchemy model representing comments on blogs or other comments (nested).

    Attributes:
        id (UUID): Unique identifier for the comment.
        content (str): The text content of the comment.
        blog_id (UUID): Foreign key referencing the blog being commented on.
        author_id (UUID): Foreign key referencing the user who wrote the comment.
        parent_comment_id (UUID, optional): Self-referencing foreign key for nested comments.
        likes (list[CommentLikeModel]): List of likes on the comment.
    """

    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(nullable=False)

    blog_id: Mapped[UUID] = mapped_column(
        ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    parent_comment_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )

    # Relationships
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="comments")
    blog: Mapped["BlogModel"] = relationship("BlogModel", back_populates="comments")

    parent_comment: Mapped["CommentModel"] = relationship(
        "CommentModel", remote_side="CommentModel.id", back_populates="replies"
    )
    replies: Mapped[list["CommentModel"]] = relationship(
        "CommentModel", back_populates="parent_comment", cascade="all, delete-orphan"
    )

    likes: Mapped[list["CommentLikeModel"]] = relationship(
        "CommentLikeModel", back_populates="comment", cascade="all, delete-orphan"
    )

    @classmethod
    def create(
        cls,
        content: str,
        author_id: UUID,
        blog_id: UUID,
        parent_comment_id: UUID | None = None,
    ) -> Self:
        """
        Factory method to create a new CommentModel instance.

        Args:
            content (str): The text content of the comment.
            author_id (UUID): The unique identifier of the user creating the comment.
            blog_id (UUID): The blog the comment belongs to.
            parent_comment_id (UUID | None): Optional parent comment for nested replies.

        Returns:
            CommentModel: A new instance of CommentModel with the provided data.
        """
        return cls(
            id=uuid.uuid4(),
            content=content,
            author_id=author_id,
            blog_id=blog_id,
            parent_comment_id=parent_comment_id,
        )
