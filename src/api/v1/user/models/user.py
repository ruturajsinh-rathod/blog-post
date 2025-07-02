import uuid
from typing import Self
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from src.core.utils.mixins import TimeStampMixin


class UserModel(Base, TimeStampMixin):
    """
    SQLAlchemy model representing a user of the system.

    Attributes:
        id (UUID): Unique identifier for the user.
        email (str): Unique email address of the user.
        password (str): Hashed password for authentication.
        role_id (UUID): Foreign key referencing the user's role.
        role (RoleModel): Relationship to the user's role.
        blogs (list[BlogModel]): List of blogs authored by the user.
    """

    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["RoleModel"] = relationship("RoleModel", back_populates="users")

    # foreign key for blog
    blogs: Mapped[list["BlogModel"]] = relationship(
        "BlogModel", back_populates="author"
    )

    likes: Mapped[list["LikeModel"]] = relationship(
        "LikeModel", back_populates="user", cascade="all, delete-orphan"
    )

    comments: Mapped[list["CommentModel"]] = relationship(
        "CommentModel", back_populates="author", cascade="all, delete-orphan"
    )

    comment_likes: Mapped[list["CommentLikeModel"]] = relationship(
        "CommentLikeModel", back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    def create(cls, email: EmailStr, password: str, role_id: UUID) -> Self:
        """
        Factory method to create a new UserModel instance.

        Args:
            email (EmailStr): The email address of the user.
            password (str): The hashed password for the user.
            role_id (UUID): The unique identifier of the user's role.

        Returns:
            UserModel: A new instance of UserModel with the provided data.
        """
        return cls(id=uuid.uuid4(), email=email, password=password, role_id=role_id)
