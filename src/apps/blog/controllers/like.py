from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Path

from apps.blog.schemas import BlogResponse, CreateBlogRequest
from apps.blog.services.blog import BlogService
from apps.blog.services.like import LikeService
from apps.user.models.user import UserModel
from core.auth import get_current_user
from core.utils.schema import BaseResponse

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post(
    "/{blog_id}",
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
    Create a new blog post.

    Args:
        user (UserModel): The currently authenticated user.
        request (CreateBlogRequest): The request body containing blog details.
        service (BlogService): The blog service for handling business logic.

    Returns:
        BaseResponse[BlogResponse]: The response containing the created blog details.
    """

    return BaseResponse(
        data=await service.create(user=user, blog_id=blog_id),
        code=status.HTTP_201_CREATED,
    )
