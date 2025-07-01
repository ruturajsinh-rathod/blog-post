from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from database.db import db_session
from src.api.v1.auth.utils.hashing import hash_password
from src.api.v1.user.exceptions import UserAlreadyExists, UserRoleNotFound
from src.api.v1.user.models import RoleModel
from src.api.v1.user.models.user import UserModel


class UserService:
    """
    Service class to handle user-related operations such as authentication and account creation.
    """

    def __init__(self, session: Annotated[AsyncSession, Depends(db_session)]) -> None:
        """
        Initialize the UserService with a database session.

        Args:
            session (AsyncSession): An asynchronous SQLAlchemy session injected via dependency.
        """
        self.session = session

    async def create(self, role_id: UUID, email: str, password: str) -> UserModel:
        """
        Create a new user account in the system.

        Args:
            role_id (UUID): The unique identifier of the role to assign to the user.
            email (str): The email address for the new user. Must be unique.
            password (str): The plain-text password for the user, which will be hashed before storing.

        Raises:
            UserRoleNotFound: If the provided role ID does not correspond to an existing role.
            UserAlreadyExists: If a user with the provided email already exists.

        Returns:
            UserModel: The newly created user instance.
        """

        role = await self.session.scalar(
            select(RoleModel).where(RoleModel.id == role_id)
        )

        if not role:
            raise UserRoleNotFound

        user = await self.session.scalar(
            select(UserModel)
            .options(load_only(UserModel.id))
            .where(UserModel.email == email)
        )
        if user:
            raise UserAlreadyExists

        hashed_pwd = await hash_password(password)

        user = UserModel.create(email=email, password=hashed_pwd, role_id=role_id)
        user.role = role

        self.session.add(user)
        return user
