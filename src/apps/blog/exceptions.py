import constants
from core.exceptions import AlreadyExistsError, NotFoundError, UnauthorizedError


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
