from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from fastapi_pagination import Page, Params

from apps.blog.schemas import BlogResponse, CreateBlogRequest
from apps.blog.services.blog import BlogService
from apps.user.enums import RoleEnum
from apps.user.models.user import UserModel
from core.auth import get_current_user, role_required
from core.utils.schema import BaseResponse

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="Create blog",
    description="Create blog",
    operation_id="create_blog",
)
async def create_blog(
    user: Annotated[UserModel, Depends(get_current_user)],
    request: CreateBlogRequest,
    service: Annotated[BlogService, Depends()],
) -> BaseResponse[BlogResponse]:
    """
    Create a new blog post.

    Args:
        user (UserModel): The currently authenticated user.
        request (CreateBlogRequest): The request body containing blog details.
        service (BlogService): The blog service for handling business logic.

    Returns:
        BaseResponse[BlogResponse]: The response containing the created blog details.
    """

    return BaseResponse(
        data=await service.create_blog(user=user, **request.model_dump()),
        code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="Get all blogs",
    description="Get all blogs",
    operation_id="get_all_blogs",
    response_model=Page[BlogResponse],
)
async def get_all(
    _: Annotated[bool, Depends(get_current_user)],
    service: Annotated[BlogService, Depends()],
    params: Params = Depends(),
) -> Page[BlogResponse]:
    """
    Retrieve a paginated list of all blogs.

    Args:
        _ (bool): The authenticated user, used for access control.
        service (BlogService): Service handling blog-related business logic.
        params (Params): Pagination parameters (page, size).

    Returns:
        Page[BlogResponse]: A paginated list of blogs.
    """

    return await service.get_all(params=params)


@router.get(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    name="Get blog by id",
    description="Get blog by id",
    operation_id="get_blog_by_id",
)
async def get_by_id(
    _: Annotated[bool, Depends(get_current_user)],
    blog_id: Annotated[UUID, Path()],
    service: Annotated[BlogService, Depends()],
) -> BaseResponse[BlogResponse]:
    """
    Retrieve details of a specific blog by its ID.

    Args:
        _ (bool): The authenticated user, used for access control.
        blog_id (UUID): The unique identifier of the blog.
        service (BlogService): Service handling blog-related business logic.

    Returns:
        BaseResponse[BlogResponse]: The response containing blog details.
    """

    return BaseResponse(
        data=await service.get_by_id(blog_id),
        code=status.HTTP_200_OK,
    )


@router.delete(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    name="Delete blog by id",
    description="Delete blog by id",
    operation_id="delete_blog_by_id",
)
async def delete_by_id(
    _: Annotated[UserModel, role_required(RoleEnum.ADMIN)],
    blog_id: Annotated[UUID, Path()],
    service: Annotated[BlogService, Depends()],
) -> BaseResponse:
    """
    Delete a specific blog by its ID. Only accessible to admin users.

    Args:
        _ (UserModel): The authenticated admin user.
        blog_id (UUID): The unique identifier of the blog to be deleted.
        service (BlogService): Service handling blog-related business logic.

    Returns:
        BaseResponse: The response indicating successful deletion.
    """

    return BaseResponse(
        data=await service.delete_by_id(blog_id),
        code=status.HTTP_200_OK,
    )
