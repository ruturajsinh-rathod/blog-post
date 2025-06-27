from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from apps import RoleModel
from apps.user.enums import RoleEnum
from apps.user.exceptions import UserRoleAlreadyExists, UserRoleNotFound
from core.db import db_session


class RoleService:
    """
    Service class to handle role-related operations, such as creating roles
    and retrieving all available roles.
    """

    def __init__(self, session: Annotated[AsyncSession, Depends(db_session)]) -> None:
        """
        Initialize the RoleService with a database session.

        Args:
            session (AsyncSession): An asynchronous SQLAlchemy session injected via dependency.
        """
        self.session = session

    async def create(
        self, name: str
    ) -> RoleModel:
        """
                Create a new role in the system.

                Args:
                    name (str): The name of the role to be created. Must match a valid RoleEnum value.

                Raises:
                    UserRoleNotFound: If the provided role name does not exist in RoleEnum.
                    UserRoleAlreadyExists: If a role with the same name already exists in the database.

                Returns:
                    RoleModel: The newly created RoleModel instance.
        """

        if name not in [r.value for r in RoleEnum]:
            raise UserRoleNotFound

        role = await self.session.scalar(
            select(RoleModel)
            .options(load_only(RoleModel.id))
            .where(
                    RoleModel.name == name
            )
        )
        if role:
            raise UserRoleAlreadyExists

        role = RoleModel.create(
             name=name
        )
        self.session.add(role)

        return role

    async def get_all(self) -> Sequence[RoleModel]:
        """
        Retrieve all roles from the database.

        Returns:
            Sequence[RoleModel]: A list of all available role records.
        """
        result = await self.session.scalars(
            select(RoleModel)
        )
        return result.all()
