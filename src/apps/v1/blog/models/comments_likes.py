import uuid
from datetime import datetime, timezone
from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


class CommentLikeModel(Base):
    """
    SQLAlchemy model representing likes on comments by users.

    Attributes:
        id (UUID): Unique identifier for the like.
        user_id (UUID): Foreign key referencing the user who liked the comment.
        comment_id (UUID): Foreign key referencing the comment.
        created_at (datetime): Timestamp when the like was created.
    """

    __tablename__ = "comment_likes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    comment_id: Mapped[UUID] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.now(),
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="comment_likes"
    )
    comment: Mapped["CommentModel"] = relationship(
        "CommentModel", back_populates="likes"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "comment_id", name="unique_user_comment_like"),
    )

    @classmethod
    def create(cls, user_id: UUID, comment_id: UUID) -> Self:
        """
        Factory method to create a new CommentLikeModel instance.

        Args:
            user_id (UUID): The unique identifier of the user liking the comment.
            comment_id (UUID): The unique identifier of the comment being liked.

        Returns:
            CommentLikeModel: A new instance of CommentLikeModel with the provided data.
        """
        return cls(id=uuid.uuid4(), user_id=user_id, comment_id=comment_id)
