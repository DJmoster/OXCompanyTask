from fastapi import HTTPException
from starlette import status

NO_UPDATES_PROVIDED_EXCEPTION = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="No updates provided",
)
