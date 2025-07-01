from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, status

from src.api.v1.user.enums import RoleEnum
from src.api.v1.user.models.user import UserModel
from src.api.v1.user.schemas.request import CreateUserRoleRequest
from src.api.v1.user.schemas.response import RoleResponse
from src.api.v1.user.services.roles import RoleService
from src.core.auth import role_required
from src.core.basic_auth import basic_auth
from src.core.utils.schema import BaseResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="create",
    description="Create role",
    operation_id="create_role",
)
async def create_role(
    _: Annotated[bool, Depends(basic_auth)],
    request: Annotated[CreateUserRoleRequest, Body()],
    service: Annotated[RoleService, Depends()],
) -> BaseResponse[RoleResponse]:
    """
    Create a new role in the system.

    Only accessible to users with ADMIN role.

    Args:
        _: The authenticated admin user (injected by role_required).
        request (CreateUserRoleRequest): The request body containing the role name.
        service (RoleService): The role service dependency.

    Returns:
        BaseResponse[RoleResponse]: The created role information.
    """
    return BaseResponse(
        data=await service.create(**request.model_dump()),
        code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="get all",
    description="Get all roles",
    operation_id="get_all_roles",
)
async def get_roles(
    _: Annotated[UserModel, role_required(RoleEnum.ADMIN)],
    service: Annotated[RoleService, Depends()],
) -> BaseResponse[List[RoleResponse]]:
    """
    Retrieve a list of all roles in the system.

    Only accessible to users with ADMIN role.

    Args:
        _: The authenticated admin user (injected by role_required).
        service (RoleService): The role service dependency.

    Returns:
        BaseResponse[List[RoleResponse]]: A list of all roles.
    """
    return BaseResponse(
        data=await service.get_all(),
        code=status.HTTP_200_OK,
    )
