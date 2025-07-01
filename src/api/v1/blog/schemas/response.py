from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from src.core.utils import CamelCaseModel


class BlogResponse(CamelCaseModel):
    """
    Response schema representing a blog post.

    Attributes:
        id (UUID): Unique identifier of the blog post.
        name (str): Title or name of the blog post.
        author_id (UUID): Unique identifier of the author who created the blog post.
        created_at (datetime): Timestamp when the blog post was created.
        updated_at (datetime): Timestamp when the blog post was last updated.
    """

    id: UUID
    name: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime


class UserResponse(CamelCaseModel):
    """
    Response schema representing a user's public information.

    Attributes:
        id (UUID): Unique identifier of the user.
        email (EmailStr): The email address of the user.
    """

    id: UUID
    email: EmailStr

    model_config = {"from_attributes": True}


class LikeResponse(CamelCaseModel):
    """
    Response model representing the result of a like or unlike action on a blog post.

    Attributes:
        blog_id (UUID): The unique identifier of the blog post.
        like (bool): Indicates whether the post is liked (True) or unliked (False) after the action.
    """

    blog_id: UUID
    like: bool


class UserLikedResponse(CamelCaseModel):
    """
    Response model containing blog like details.

    Attributes:
        blog_id (UUID): The unique identifier of the blog.
        users (list[UserResponse]): List of users who liked the blog.
        total_likes (int): Total number of likes on the blog.
    """

    blog_id: UUID
    user: list[UserResponse]
    total_likes: int


class BaseCommentResponse(CamelCaseModel):
    """
    Base response model for a comment.

    Attributes:
        id (UUID): Unique identifier of the comment.
        content (str): Text content of the comment.
        author_id (UUID): Unique identifier of the comment's author.
    """

    id: UUID
    content: str
    author_id: UUID


class CommentResponse(BaseCommentResponse):
    """
    Response model for a blog comment.

    Extends BaseCommentResponse to include blog and parent comment details.

    Attributes:
        blog_id (UUID): Unique identifier of the blog the comment belongs to.
        parent_comment_id (UUID | None): Optional parent comment ID if this is a reply.
    """

    blog_id: UUID
    parent_comment_id: UUID | None = None


class BlogCommentResponse(BlogResponse):
    """
    Response model for a blog including its comments.

    Attributes:
        comments (list[BaseCommentResponse]): List of top-level comments on the blog.
    """

    comments: list[BaseCommentResponse]


class ReplyResponse(CamelCaseModel):
    """
    Response model for a comment reply.

    Attributes:
        id (UUID): Unique identifier of the reply.
        content (str): Text content of the reply.
        author_id (UUID): Unique identifier of the reply's author.
    """

    id: UUID
    content: str
    author_id: UUID


class CommentLikeResponse(CamelCaseModel):
    """
    Response model for like status on a comment.

    Attributes:
        comment_id (UUID): Unique identifier of the comment.
        like (bool): Indicates if the current user has liked the comment.
    """

    comment_id: UUID
    like: bool
