from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.apps.v1.auth.services.auth import AuthService
from src.apps.v1.user.schemas import LoginRequest, LoginResponse
from src.apps.v1.user.schemas.response import RefreshTokenResponse
from src.core.utils.schema import BaseResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    name="Login",
    description="Login user",
    operation_id="login_user",
)
async def login(
    request: Annotated[LoginRequest, Body()], service: Annotated[AuthService, Depends()]
) -> BaseResponse[LoginResponse]:
    """
    Authenticate a user with email and password and return a JWT access token.

    Args:
        request (LoginRequest): The login request containing email and password.
        service (AuthService): The auth service dependency.

    Returns:
        BaseResponse[LoginResponse]: The access token upon successful authentication.
    """
    return BaseResponse(
        data=await service.login(**request.model_dump()), code=status.HTTP_201_CREATED
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    name="Refresh",
    description="Create refresh token",
    operation_id="refresh_token",
)
async def refresh_token(
    service: Annotated[AuthService, Depends()],
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> BaseResponse[RefreshTokenResponse]:
    """
    Generate a new access token using a valid refresh token.

    This endpoint accepts a valid refresh token via the Authorization header
    and returns a newly generated access token for continued authenticated access.

    Args:
        service (AuthService): The authentication service instance provided via dependency injection.
        credentials (HTTPAuthorizationCredentials): The security credentials extracted from the Authorization header.

    Returns:
        BaseResponse[RefreshTokenResponse]: A response containing the new access token.
    """

    return BaseResponse(
        data=await service.refresh(credentials), code=status.HTTP_201_CREATED
    )
