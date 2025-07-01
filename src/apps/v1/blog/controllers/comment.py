from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.apps.v1.blog.schemas.response import CommentLikeResponse, ReplyResponse
from src.apps.v1.blog.services.comment import CommentService
from src.apps.v1.user.models.user import UserModel
from src.core.auth import get_current_user
from src.core.utils.schema import BaseResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/{comment_id}/replies",
    status_code=status.HTTP_200_OK,
    name="Get replies",
    description="Get replies",
    operation_id="get_replies",
)
async def get_replies(
    _: Annotated[UserModel, Depends(get_current_user)],
    comment_id: Annotated[UUID, Path()],
    service: Annotated[CommentService, Depends()],
) -> BaseResponse[list[ReplyResponse]]:
    """
    Retrieve replies for a comment.

    This endpoint returns the list of replies for the specified parent comment.

    Args:
        _ (UserModel): The currently authenticated user (authorization only).
        comment_id (UUID): The unique identifier of the parent comment.
        service (CommentService): The comment service handling business logic.

    Returns:
        BaseResponse[list[ReplyResponse]]: A response containing the list of replies.
    """
    return BaseResponse(
        data=await service.get_replies(comment_id=comment_id),
        code=status.HTTP_200_OK,
    )


@router.post(
    "/{comment_id}/like",
    status_code=status.HTTP_201_CREATED,
    name="Like or unlike comment",
    description="like or unlike comment",
    operation_id="like_or_unlike_comment",
    response_model=BaseResponse[CommentLikeResponse],
)
async def like_or_unlike_comment(
    user: Annotated[UserModel, Depends(get_current_user)],
    comment_id: Annotated[UUID, Path()],
    service: Annotated[CommentService, Depends()],
) -> BaseResponse[CommentLikeResponse]:
    """
    Like or unlike a comment.

    This endpoint allows an authenticated user to like or unlike the specified comment.
    If the user has already liked the comment, the like will be removed (unlike).
    Otherwise, the comment will be liked.

    Args:
        user (UserModel): The currently authenticated user.
        comment_id (UUID): The unique identifier of the comment.
        service (CommentService): The comment service handling business logic.

    Returns:
        BaseResponse[CommentLikeResponse]: A response containing the updated like status.
    """
    return BaseResponse(
        data=await service.like_or_unlike_comment(user=user, comment_id=comment_id),
        code=status.HTTP_200_OK,
    )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    name="remove comment",
    description="remove comment",
    operation_id="remove_comment",
    response_model=BaseResponse,
)
async def remove_comment(
    user: Annotated[UserModel, Depends(get_current_user)],
    comment_id: Annotated[UUID, Path()],
    service: Annotated[CommentService, Depends()],
) -> BaseResponse:
    """
    Delete a comment.

    This endpoint allows the author of a comment to delete it.
    Only the comment's author or authorized users can perform this action.

    Args:
        user (UserModel): The currently authenticated user.
        comment_id (UUID): The unique identifier of the comment to delete.
        service (CommentService): The comment service handling business logic.

    Returns:
        BaseResponse: A response confirming successful deletion of the comment.
    """
    return BaseResponse(
        data=await service.remove_comment(user=user, comment_id=comment_id),
        code=status.HTTP_200_OK,
    )
