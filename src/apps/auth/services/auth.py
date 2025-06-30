from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from apps.enums import TokenTypeEnum
from apps.user.exceptions import UserNotFound
from apps.user.models.user import UserModel
from apps.user.schemas import LoginResponse
from apps.user.schemas.response import RefreshTokenResponse
from core.auth import create_token, decode_token
from core.db import db_session
from core.utils.hashing import verify_password

security = HTTPBearer()

class AuthService:
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

    async def login(self, email: str, password: str) -> LoginResponse:
        """
        Authenticate a user using their email and password.

        Args:
            email (str): The email address of the user attempting to log in.
            password (str): The plain-text password provided for verification.

        Raises:
            UserNotFound: If no user is found with the provided email or if the password is incorrect.

        Returns:
            LoginResponse: Contains a JWT access token upon successful authentication.
        """

        user_query = (
            select(UserModel)
            .options(
                load_only(
                    UserModel.email,
                    UserModel.password,
                )
            )
            .where(UserModel.email == email)
        )

        user = await self.session.scalar(user_query)

        if not user:
            raise UserNotFound

        if not await verify_password(password, user.password):
            raise UserNotFound

        access_token = create_token(email=user.email, token_type=TokenTypeEnum.ACCESS)
        refresh_token = create_token(email=user.email, token_type=TokenTypeEnum.REFRESH)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> RefreshTokenResponse:
        """
            Refresh the access token using a valid refresh token.

            This method validates the provided refresh token, extracts the payload,
            and generates a new access token for the user.

            Args:
                credentials (HTTPAuthorizationCredentials): The security credentials extracted
                    from the Authorization header, containing the refresh token.

            Returns:
                RefreshTokenResponse: An object containing the newly generated access token.

            Raises:
                HTTPException: If the refresh token is invalid, expired, or of an incorrect type.
        """

        refresh_token = credentials.credentials

        payload = decode_token(refresh_token, expected_type=TokenTypeEnum.REFRESH)

        new_access_token = create_token(payload["sub"], TokenTypeEnum.ACCESS)

        return RefreshTokenResponse(access_token=new_access_token)
