import enum


class RoleEnum(str, enum.Enum):
    """
    Enumeration of possible user roles within the system.

    Attributes:
        ADMIN (str): Represents an administrative user with elevated permissions.
        USER (str): Represents a regular user with standard permissions.
    """

    ADMIN = "ADMIN"
    USER = "USER"
