from pydantic import BaseModel, EmailStr


class CreateBlogRequest(BaseModel):
    """
    Request schema for creating a new blog post.

    Attributes:
        name (str): The title or name of the blog post.
        content (str): The content or body of the blog post.
    """

    name: str
    content: str
