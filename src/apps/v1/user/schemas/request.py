from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    """
    Request schema for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        password (str): The plain-text password for the user. Should be hashed before storing.
        role_id (UUID): The unique identifier of the role to assign to the user.
    """

    email: EmailStr
    password: str
    role_id: UUID


class CreateUserRoleRequest(BaseModel):
    """
    Request schema for creating a new user role.

    Attributes:
        name (str): The name of the role to be created. Should be unique and descriptive.
    """

    name: str


class LoginRequest(BaseModel):
    """
    Request schema for user login.

    Attributes:
        email (EmailStr): The registered email address of the user.
        password (str): The plain-text password of the user.
    """

    email: EmailStr
    password: str
