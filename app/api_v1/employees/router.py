import starlette.status

from fastapi import APIRouter, Depends
from typing import Annotated

from psycopg2.extras import RealDictCursor

from app.database.database import db_helper

from ..auth.annotations import role_requiered
from ..auth.dependencies import get_current_auth_user
from ..auth.schemas import AuthSchema
from ..auth.enums import AuthRole

from .schemas import (
    EmployeeCreate,
    EmployeeSchema,
    EmployeeUpdate,
    EmployeeWithPasswordSchema,
)
from .service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", status_code=starlette.status.HTTP_201_CREATED)
@role_requiered([AuthRole.ADMIN, AuthRole.MODERATOR])
async def create(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_in: EmployeeCreate,
) -> EmployeeSchema | EmployeeWithPasswordSchema:
    _service = EmployeeService(cursor)

    return await _service.create(employee_in)


@router.get("/")
@role_requiered([AuthRole.ADMIN, AuthRole.MODERATOR, AuthRole.USER])
async def get_all_employees(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    page: int = 1,
    page_size: int = 10,
) -> list[EmployeeSchema]:
    _service = EmployeeService(cursor)

    return await _service.get_all(page, page_size)


@router.get("/{employee_id}")
@role_requiered([AuthRole.ADMIN, AuthRole.MODERATOR, AuthRole.USER])
async def get_employee_by_id(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
) -> EmployeeSchema:
    _service = EmployeeService(cursor)

    return await _service.get_by_id(employee_id)


@router.patch("/{employee_id}")
@role_requiered([AuthRole.ADMIN, AuthRole.MODERATOR])
async def update_employee_by_id(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
    employee_in: EmployeeUpdate,
) -> EmployeeSchema:
    _service = EmployeeService(cursor)

    return await _service.update_by_id(employee_id, employee_in)


@router.delete("/{employee_id}", status_code=starlette.status.HTTP_204_NO_CONTENT)
@role_requiered([AuthRole.ADMIN, AuthRole.MODERATOR])
async def delete_employee_by_id(
    cursor: Annotated[RealDictCursor, Depends(db_helper.cursor_dependency)],
    current_user: Annotated[AuthSchema, Depends(get_current_auth_user)],
    employee_id: int,
) -> None:
    _service = EmployeeService(cursor)

    return await _service.delete_by_id(employee_id)
