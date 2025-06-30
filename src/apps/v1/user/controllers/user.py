from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from apps.v1.user.schemas import CreateUserRequest, LoginRequest, LoginResponse, UserResponse
from apps.v1.user.services import UserService
from core.utils.schema import BaseResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    name="create",
    description="Create user",
    operation_id="create_user",
)
async def create_user(
    request: Annotated[CreateUserRequest, Body()],
    service: Annotated[UserService, Depends()],
) -> BaseResponse[UserResponse]:
    """
    Register a new user account in the system.

    Args:
        request (CreateUserRequest): The registration request containing email, password, and role ID.
        service (UserService): The user service dependency.

    Returns:
        BaseResponse[UserResponse]: The created user's public information.
    """
    return BaseResponse(
        data=await service.create(**request.model_dump()),
        code=status.HTTP_201_CREATED,
    )
