from fastapi import HTTPException
from starlette import status

EMAIL_OR_PHONE_ALREADY_USED_EXCEPTION = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Email or phone is already used",
)

EMPLOYEE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Employee not found",
)
