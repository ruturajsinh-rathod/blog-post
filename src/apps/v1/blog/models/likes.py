import uuid
from datetime import datetime, timezone
from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


class LikeModel(Base):
    """
    SQLAlchemy model representing a Like on a blog post by a user.

    Attributes:
        id (UUID): Unique identifier for the like.
        user_id (UUID): Foreign key referencing the user who liked the blog.
        post_id (UUID): Foreign key referencing the blog post.
        created_at (datetime): Timestamp when the like was created.
    """

    __tablename__ = "likes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    blog_id: Mapped[UUID] = mapped_column(
        ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.now(),
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="likes")
    blog: Mapped["BlogModel"] = relationship("BlogModel", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "blog_id", name="unique_user_blog_like"),
    )

    @classmethod
    def create(cls, user_id: UUID, blog_id: UUID) -> Self:
        """
        Factory method to create a new UserModel instance.

        Args:
            email (EmailStr): The email address of the user.
            password (str): The hashed password for the user.
            role_id (UUID): The unique identifier of the user's role.

        Returns:
            UserModel: A new instance of UserModel with the provided data.
        """
        return cls(id=uuid.uuid4(), user_id=user_id, blog_id=blog_id)
