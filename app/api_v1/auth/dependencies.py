from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from app.database.database import db_helper

from .exceptions import INVALID_TOKEN_EXCEPTION, USER_NOT_ACTIVE_EXCEPTION
from .utils import decode_jwt
from .schemas import AuthSchema
from .repository import AuthRepository

http_bearer = HTTPBearer()


async def get_current_token_payload(
    token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:
    try:
        return decode_jwt(token.credentials)
    except InvalidTokenError:
        raise INVALID_TOKEN_EXCEPTION


async def get_current_auth_user(
    cursor: Annotated[AsyncSession, Depends(db_helper.cursor_dependency)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> AuthSchema:
    if not (auth_id := payload.get("sub")):
        raise INVALID_TOKEN_EXCEPTION

    auth_repository = AuthRepository(cursor)

    auth_record = auth_repository.get_by_id(auth_id)

    if auth_record is None or not auth_record.is_active:
        raise USER_NOT_ACTIVE_EXCEPTION

    return auth_record
