from datetime import datetime
from uuid import UUID

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


class LikeResponse(CamelCaseModel):
    """
    Response model representing the result of a like or unlike action on a blog post.

    Attributes:
        blog_id (UUID): The unique identifier of the blog post.
        like (bool): Indicates whether the post is liked (True) or unliked (False) after the action.
    """

    blog_id: UUID
    like: bool
