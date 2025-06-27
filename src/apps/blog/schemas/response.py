from datetime import datetime
from uuid import UUID

from core.utils import CamelCaseModel


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
