from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config.config import settings
from src.apps.v1.blog.exceptions import InvalidCredsException


def basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    """
    Dependency function for required basic authentication.
    It uses the HTTPBasic instance to perform authentication.

    Args:
    - credentials: HTTPBasicCredentials object containing the provided username and password.

    Returns:
    - True if authentication is successful.

    Raises:
    - InvalidCredsException: If authentication fails.
    """

    if (
        credentials.username == settings.BASIC_USERNAME
        and credentials.password == settings.BASIC_PASSWORD
    ):
        return True
    else:
        raise InvalidCredsException
