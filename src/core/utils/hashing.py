from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    """
    Hash a password.

    :param password: Password to be hashed.
    :return: Hashed password.
    """
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password.

    :param plain_password: Plain text password.
    :param hashed_password: Hashed password.
    :return: True if password is valid else False.
    """
    return pwd_context.verify(plain_password, hashed_password)
