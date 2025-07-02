from src import constants
from src.core.exceptions import AlreadyExistsError, NotFoundError, UnauthorizedError


class InvalidCredsException(UnauthorizedError):
    """
    Exception raised for invalid credentials during authentication.
    """

    message = constants.INVALID_CRED


class DuplicateBlogException(AlreadyExistsError):
    """
    Exception raised when an blog with the same name or admin email
    already exists in the system.
    """

    message = constants.DUPLICATE_BLOG


class BlogNotFoundException(NotFoundError):
    """
    Exception raised when the requested blog cannot be found.
    """

    message = constants.BLOG_NOT_FOUND


class ParentCommentNotFoundException(NotFoundError):
    """
    Exception raised when the requested parent comment cannot be found.
    """

    message = constants.PARENT_COMMENT_NOT_FOUND


class InvalidParentCommentBlogException(NotFoundError):
    """
    Exception raised when the parent comment does not belong to the same blog.
    """

    message = constants.INVALID_PARENT_COMMENT_BLOG


class InvalidParentCommentNestingException(AlreadyExistsError):
    """
    Exception raised when attempting to reply to a comment that is already a child comment.
    """

    message = constants.INVALID_PARENT_COMMENT_NESTING


class CommentNotFoundException(NotFoundError):
    """
    Exception raised when the requested comment cannot be found.
    """

    message = constants.COMMENT_NOT_FOUND
