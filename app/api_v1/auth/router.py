import starlette.status
from fastapi import APIRouter, Depends
from typing import Annotated

from psycopg2.extras import RealDictCursor

from app.database.database import db_helper

from .annotations import role_requiered
from .dependencies import get_current_auth_user
from .enums import AuthRole
from .schemas import (
    LoginUser,
    TokenResponse,
    AuthCreateResponse,
    AuthSchema,
    AuthUpdate,
    AuthUpdateResponse,
    AuthCreate,
)
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login/")
async def login(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    user_in: LoginUser,
) -> TokenResponse:
    _service = AuthService(cursor)

    return await _service.login_user(user_in)


@router.post("/employees/{employee_id}", status_code=starlette.status.HTTP_201_CREATED)
@role_requiered([AuthRole.ADMIN])
async def create_employee_auth(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
    auth_in: AuthUpdate,
) -> AuthCreateResponse:
    _service = AuthService(cursor)

    return await _service.create(employee_id, auth_in)


@router.get("/employees/{employee_id}")
@role_requiered([AuthRole.ADMIN])
async def get_employee_auth(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
) -> AuthUpdateResponse:
    _service = AuthService(cursor)

    return await _service.get_by_employee_id(employee_id)


@router.patch("/employees/{employee_id}")
@role_requiered([AuthRole.ADMIN])
async def edit_employee_auth(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
    auth_in: AuthUpdate,
) -> AuthUpdateResponse:
    _service = AuthService(cursor)

    return await _service.update_by_employee_id(employee_id, auth_in)


@router.delete(
    "/employees/{employee_id}", status_code=starlette.status.HTTP_204_NO_CONTENT
)
@role_requiered([AuthRole.ADMIN])
async def delete_employee_auth(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
) -> None:
    _service = AuthService(cursor)

    return await _service.delete_by_employee_id(employee_id)


@router.post("/employees/{employee_id}/renew")
@role_requiered([AuthRole.ADMIN])
async def renew_employee_auth_password(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
) -> AuthCreate:
    _service = AuthService(cursor)

    return await _service.renew_employee_password(employee_id)
