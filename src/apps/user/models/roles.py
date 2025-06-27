import uuid
from typing import Self, List
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.user.models.user import UserModel
from apps.user.enums import RoleEnum
from core.db import Base
from core.utils.mixins import TimeStampMixin
from sqlalchemy import Enum as SqlEnum


class RoleModel(Base, TimeStampMixin):
    """
    SQLAlchemy model representing user roles.

    Attributes:
        id (UUID): Primary key for the role.
        name (RoleEnum): Name of the role (e.g., 'ADMIN', 'USER').
        users (List[UserModel]): List of users associated with this role.
    """

    __tablename__ = "roles"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum, name="roleenum"), unique=True, nullable=False)

    users: Mapped[List["UserModel"]] = relationship(back_populates="role")

    @classmethod
    def create(cls, name: str) -> Self:
        """
        Factory method to create a new RoleModel instance.

        Args:
            name (str): The name of the role (should be a valid RoleEnum value).

        Returns:
            RoleModel: A new instance of the RoleModel with the specified name.
        """
        return cls(id=uuid.uuid4(), name=name)
