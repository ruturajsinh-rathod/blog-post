import uuid
from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from src.core.utils.mixins import TimeStampMixin


class BlogModel(Base, TimeStampMixin):
    """
    SQLAlchemy model representing a blog post.

    Attributes:
        id (UUID): Unique identifier for the blog.
        name (str): Title or name of the blog.
        content (str): Content or body of the blog.
        author_id (UUID): Foreign key referencing the blog's author.
        author (UserModel): Relationship to the UserModel representing the author.
    """

    __tablename__ = "blogs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)

    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="blogs")

    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    likes: Mapped[list["LikeModel"]] = relationship(
        "LikeModel", back_populates="blog", cascade="all, delete-orphan"
    )

    comments: Mapped[list["CommentModel"]] = relationship(
        "CommentModel", back_populates="blog", cascade="all, delete-orphan"
    )

    @classmethod
    def create(cls, name: str, content: str, author_id: UUID) -> Self:
        """
        Factory method to create a new BlogModel instance.

        Args:
            name (str): The title or name of the blog.
            content (str): The main content or body of the blog.
            author_id (UUID): The unique identifier of the author (user) creating the blog.

        Returns:
            BlogModel: A new instance of BlogModel with the provided data.
        """
        return cls(id=uuid.uuid4(), name=name, content=content, author_id=author_id)
