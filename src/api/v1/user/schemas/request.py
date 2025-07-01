import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator


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

    @validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validates password complexity:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

        if not re.match(password_regex, value):
            raise ValueError(
                "Password must be at least 8 characters long, contain an uppercase letter, "
                "a lowercase letter, a digit, and a special character."
            )
        return value


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
