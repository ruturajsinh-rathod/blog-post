from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.apps.v1.blog.schemas.response import UserLikedResponse
from src.apps.v1.blog.services.like import LikeService
from src.apps.v1.user.models.user import UserModel
from src.core.auth import get_current_user
from src.core.utils.schema import BaseResponse

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
    Like or unlike a blog post.

    If the blog post exists and the user has already liked it, the like will be removed (unlike).
    If the user has not liked the blog post yet, a new like will be created.

    Args:
        user (UserModel): The currently authenticated user.
        service (LikeService): Service handling the like logic.
        blog_id (UUID): The unique identifier of the blog post to like or unlike.

    Returns:
        BaseResponse: A standardized response containing the like status and blog ID.

    Raises:
        BlogNotFoundException: If the blog post with the given ID does not exist.
    """

    return BaseResponse(
        data=await service.create(user=user, blog_id=blog_id),
        code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{blog_id}",
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
    return BaseResponse(
        data=await service.get_likes(blog_id=blog_id),
        code=status.HTTP_200_OK,
    )
