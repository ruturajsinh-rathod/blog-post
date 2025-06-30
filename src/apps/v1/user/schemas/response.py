from uuid import UUID

from pydantic import EmailStr

from src.core.utils import CamelCaseModel


class LoginResponse(CamelCaseModel):
    """
    Response schema returned after a successful login.

    Attributes:
        access_token (str): JWT or token string used for authenticated access to protected routes.
    """

    access_token: str
    refresh_token: str


class RefreshTokenResponse(CamelCaseModel):
    """
    Response model for the token refresh operation.

    Attributes:
        access_token (str): The newly issued access token
            that can be used for authenticated requests.
    """
    access_token: str


class RoleResponse(CamelCaseModel):
    """
    Response schema representing a user's role information.

    Attributes:
        id (UUID): Unique identifier of the role.
        name (str): The name of the role.
    """

    id: UUID
    name: str


class UserResponse(CamelCaseModel):
    """
    Response schema representing a user's public information.

    Attributes:
        id (UUID): Unique identifier of the user.
        email (EmailStr): The email address of the user.
        role (RoleResponse): The role assigned to the user.
    """

    id: UUID
    email: EmailStr
    role: RoleResponse
