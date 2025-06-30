from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

import constants.messages as constants
from apps.enums import TokenTypeEnum
from apps.user.enums import RoleEnum
from apps.user.exceptions import UnauthorizedAccessException, UserNotFound
from apps.user.models.user import UserModel
from config import settings
from core.db import db_session
from core.exceptions import InvalidJWTTokenException

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXP
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXP

security = HTTPBearer()

def create_token(email: str, token_type: str):
    """
    Generate a JWT token (access or refresh) containing the user's email and token type.

    Args:
        email (str): The email of the user (subject of the token).
        token_type (str): The type of the token ('access' or 'refresh').

    Returns:
        str: The encoded JWT token as a string.
    """
    now = datetime.now(tz=timezone.utc)

    if token_type == TokenTypeEnum.ACCESS:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == TokenTypeEnum.REFRESH:
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise ValueError("Invalid token type. Must be 'access' or 'refresh'.")

    claims = {
        "sub": email,
        "aud": settings.APP_NAME,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": token_type
    }

    encoded_jwt = jwt.encode(
        claims, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str, expected_type: str):
    """
    Decode and validate a JWT token, ensuring the correct token type.

    Args:
        token (str): The JWT token string to decode.
        expected_type (str): The expected token type ('access' or 'refresh').

    Returns:
        dict: The decoded token payload (claims).

    Raises:
        InvalidJWTTokenException: If the token is invalid, expired, or incorrect type.
        HTTPException: For other JWT-related errors.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.APP_NAME,
        )

        if payload.get("type") != expected_type:
            raise InvalidJWTTokenException(constants.INVALID_TOKEN)

        return payload

    except DecodeError:
        raise InvalidJWTTokenException(constants.INVALID_TOKEN)
    except ExpiredSignatureError:
        raise InvalidJWTTokenException(constants.EXPIRED_TOKEN)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_authenticated_user(
    session: Annotated[AsyncSession, Depends(db_session)],
    credentials: HTTPAuthorizationCredentials = Depends(security),
    required_role: RoleEnum | None = None,
):
    """
    Retrieve the currently authenticated user and optionally validate their role.

    Args:
        session (AsyncSession): The asynchronous database session.
        credentials (HTTPAuthorizationCredentials): Authorization credentials (Bearer token).
        required_role (RoleEnum | None): Optional role to validate against the user's role.

    Returns:
        UserModel: The authenticated user.

    Raises:
        UserNotFound: If the user is not found in the database.
        UnauthorizedAccessException: If the user's role does not match the required role.
    """
    token = credentials.credentials
    payload = decode_token(token, expected_type=TokenTypeEnum.ACCESS)
    email = payload.get("sub")

    user = await session.scalar(
        select(UserModel)
        .options(joinedload(UserModel.role))
        .where(UserModel.email == email)
    )

    if not user:
        raise UserNotFound

    if required_role and user.role.name != required_role:
        raise UnauthorizedAccessException

    return user


async def get_current_user(
    session: Annotated[AsyncSession, Depends(db_session)],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Dependency to retrieve the currently authenticated user.

    Args:
        session (AsyncSession): The asynchronous database session.
        credentials (HTTPAuthorizationCredentials): Authorization credentials (Bearer token).

    Returns:
        UserModel: The authenticated user.
    """

    return await get_authenticated_user(session, credentials)


def role_required(required_role: RoleEnum):
    """
    Dependency generator to restrict route access based on the user's role.

    Args:
        required_role (RoleEnum): The role required to access the route.

    Returns:
        Depends: A FastAPI dependency that validates the user's role and returns the authenticated user.

    Raises:
        UserNotFound: If the user is not found in the database.
        UnauthorizedAccessException: If the user's role does not match the required role.
    """

    async def dependency(
        session: Annotated[AsyncSession, Depends(db_session)],
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        return await get_authenticated_user(
            session, credentials, required_role=required_role
        )

    return Depends(dependency)
