from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation

from app.base import BaseService

from ..auth.schemas import AuthUpdate
from ..auth.service import AuthService
from ..auth.enums import AuthRole

from .repository import EmployeeRepository
from .schemas import (
    EmployeeSchema,
    EmployeeUpdate,
    EmployeeCreate,
    EmployeeWithPasswordSchema,
)
from .enums import EmployeePosition
from .exceptions import (
    EMAIL_OR_PHONE_ALREADY_USED_EXCEPTION,
    EMPLOYEE_NOT_FOUND_EXCEPTION,
)


class EmployeeService(BaseService):
    def __init__(self, cursor: RealDictCursor):
        super().__init__(cursor)

        self.__employee_repository = EmployeeRepository(cursor)
        self.__auth_service = AuthService(cursor)

    async def create(self, obj: EmployeeCreate) -> EmployeeSchema:
        try:
            employee_record = self.__employee_repository.create(obj)
        except UniqueViolation:
            raise EMAIL_OR_PHONE_ALREADY_USED_EXCEPTION

        if obj.position == EmployeePosition.HUMAN_RESOURCES:
            auth_responce = await self.__auth_service.create(
                employee_record.id,
                AuthUpdate(
                    role=AuthRole.USER,
                    is_active=True,
                ),
            )

            res = dict(employee_record)
            res["password"] = auth_responce.password

            return EmployeeWithPasswordSchema.model_validate(res)

        return EmployeeSchema.model_validate(dict(employee_record))

    async def get_by_id(self, obj_id: int) -> EmployeeSchema:
        if not (employee_record := self.__employee_repository.get_by_id(obj_id)):
            raise EMPLOYEE_NOT_FOUND_EXCEPTION

        return employee_record

    async def get_all(self, page: int, page_size: int) -> list[EmployeeSchema]:
        return self.__employee_repository.get_all(page, page_size)

    async def update_by_id(
        self, obj_id: int, obj_update: EmployeeUpdate
    ) -> EmployeeSchema:
        if not (
            employee_record := self.__employee_repository.update_by_id(
                obj_id, obj_update
            )
        ):
            raise EMPLOYEE_NOT_FOUND_EXCEPTION
        return employee_record

    async def delete_by_id(self, obj_id: int) -> None:
        return self.__employee_repository.delete_by_id(obj_id)
