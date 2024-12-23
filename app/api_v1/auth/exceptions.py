from fastapi import HTTPException
from starlette import status

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid auth token",
)

INVALID_EMAIL_OR_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
)

USER_NOT_ACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not active",
)

USER_NOT_PERMITTED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not permitted",
)

USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

USER_CREDENTIALS_ALREARY_CREATED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User credentials is already created",
)
