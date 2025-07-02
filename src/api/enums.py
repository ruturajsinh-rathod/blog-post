import enum


class TokenTypeEnum(str, enum.Enum):
    """
    Enumeration of possible token types within the system.

    Attributes:
        ACCESS (str): Represents an access token, typically short-lived and used for authentication.
        REFRESH (str): Represents a refresh token, used to obtain new access tokens.
    """

    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
