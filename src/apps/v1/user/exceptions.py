import src.constants as constants
from src.core.exceptions import AlreadyExistsError, NotFoundError, UnauthorizedError


class InvalidCredsException(UnauthorizedError):
    """
    Raised when the provided login credentials are invalid.
    """

    message = constants.INVALID_CRED


class UserNotFound(NotFoundError):
    """
    Raised when a user with the specified identifier or email is not found in the database.
    """

    message = constants.USER_NOT_FOUND


class UserAlreadyExists(AlreadyExistsError):
    """
    Raised when a user with the same email already exists in the system.
    """

    message = constants.USER_FOUND


class UserRoleAlreadyExists(AlreadyExistsError):
    """
    Raised when a user role with the same name already exists in the system.
    """

    message = constants.USER_ROLE_FOUND


class UserRoleNotFound(NotFoundError):
    """
    Raised when the specified user role is not found in the system.
    """

    message = constants.USER_ROLE_NOT_FOUND


class UnauthorizedAccessException(UnauthorizedError):
    """
    Raised when a user attempts to access a resource they are not authorized for.
    """

    message = constants.UNAUTHORIZEDACCESS
