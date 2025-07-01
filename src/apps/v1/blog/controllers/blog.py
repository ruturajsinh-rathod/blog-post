from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from fastapi_pagination import Page, Params

from src.apps.v1.blog.schemas import BlogResponse, CreateBlogRequest
from src.apps.v1.blog.schemas.request import CreateCommentRequest
from src.apps.v1.blog.schemas.response import BlogCommentResponse, CommentResponse, UserLikedResponse
from src.apps.v1.blog.services.blog import BlogService
from src.apps.v1.blog.services.comment import CommentService
from src.apps.v1.blog.services.like import LikeService
from src.apps.v1.user.enums import RoleEnum
from src.apps.v1.user.models.user import UserModel
from src.core.auth import get_current_user, role_required
from src.core.utils.schema import BaseResponse

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


@router.post(
    "/{blog_id}/comments",
    status_code=status.HTTP_201_CREATED,
    name="Create comment",
    description="Create comment",
    operation_id="create_comment",
)
async def create_comment(
    user: Annotated[UserModel, Depends(get_current_user)],
    blog_id: Annotated[UUID, Path()],
    request: CreateCommentRequest,
    service: Annotated[CommentService, Depends()],
) -> BaseResponse[CommentResponse]:
    """
    Create a new comment on a blog.

    This endpoint allows an authenticated user to create a comment on the specified blog.
    If `parent_comment_id` is provided in the request, the comment will be created as a reply to the specified parent comment.

    Args:
        user (UserModel): The currently authenticated user.
        blog_id (UUID): The unique identifier of the blog to comment on.
        request (CreateCommentRequest): The request body containing the comment content and optional parent comment ID.
        service (CommentService): The comment service handling business logic.

    Returns:
        BaseResponse[CommentResponse]: The created comment wrapped in a standard API response.
    """
    return BaseResponse(
        data=await service.create_comment(
            blog_id=blog_id, user=user, **request.model_dump()
        ),
        code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{blog_id}/comments",
    status_code=status.HTTP_201_CREATED,
    name="Get top level comments",
    description="Get top level comments",
    operation_id="get_top_level_comments",
)
async def get_parent_comments(
    _: Annotated[UserModel, Depends(get_current_user)],
    blog_id: Annotated[UUID, Path()],
    service: Annotated[CommentService, Depends()],
) -> BaseResponse[BlogCommentResponse]:
    """
    Retrieve top-level comments for a blog.

    This endpoint returns all first-level (parent) comments for the specified blog.
    Nested replies are not included in this response.

    Args:
        _ (UserModel): The currently authenticated user (authorization only).
        blog_id (UUID): The unique identifier of the blog to retrieve comments for.
        service (CommentService): The comment service handling business logic.

    Returns:
        BaseResponse[BlogCommentResponse]: A list of top-level comments wrapped in a standard API response.
    """
    return BaseResponse(
        data=await service.get_parent_comments(blog_id=blog_id),
        code=status.HTTP_200_OK,
    )


@router.post(
    "/{blog_id}/like",
    status_code=status.HTTP_201_CREATED,
    name="Create like",
    description="Create like",
    operation_id="create_like",
)
async def create(
    user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[LikeService, Depends()],
    blog_id: Annotated[UUID, Path()],
) -> BaseResponse:
    """
    Like a blog post.

    This endpoint allows an authenticated user to like the specified blog.
    If the user has already liked the blog, the service may either ignore the request or return an appropriate response depending on your business logic.

    Args:
        user (UserModel): The currently authenticated user.
        service (LikeService): The service handling like creation logic.
        blog_id (UUID): The unique identifier of the blog to be liked.

    Returns:
        BaseResponse: Standard API response containing the result of the like operation.
    """
    return BaseResponse(
        data=await service.create(user=user, blog_id=blog_id),
        code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{blog_id}/like",
    status_code=status.HTTP_200_OK,
    name="Get likes of blog",
    description="Get likes of blog",
    operation_id="get_likes",
)
async def get_likes(
    _: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[LikeService, Depends()],
    blog_id: Annotated[UUID, Path()],
) -> BaseResponse[UserLikedResponse]:
    """
    Retrieve like information for a blog.

    This endpoint returns information about the likes of a specific blog,
    such as the total number of likes and whether the current user has liked the blog.

    Args:
        _ (UserModel): The currently authenticated user (authorization only).
        service (LikeService): The service handling like retrieval logic.
        blog_id (UUID): The unique identifier of the blog to retrieve like information for.

    Returns:
        BaseResponse[UserLikedResponse]: A response containing the like details for the blog.
    """
    return BaseResponse(
        data=await service.get_likes(blog_id=blog_id),
        code=status.HTTP_200_OK,
    )
