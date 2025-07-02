from uuid import UUID

from pydantic import BaseModel


class CreateBlogRequest(BaseModel):
    """
    Request schema for creating a new blog post.

    Attributes:
        name (str): The title or name of the blog post.
        content (str): The content or body of the blog post.
    """

    name: str
    content: str


class CreateCommentRequest(BaseModel):
    """
    Request model for creating a comment on a blog.

    Attributes:
        content (str): The text content of the comment.
        parent_comment_id (UUID | None): Optional ID of the parent comment
            if the comment is a reply. Defaults to None for top-level comments.
    """

    content: str
    parent_comment_id: UUID | None = None
