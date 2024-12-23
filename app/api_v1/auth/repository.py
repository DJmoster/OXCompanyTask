from typing import Any

from app.base import BaseRepository

from .schemas import AuthSchema, AuthCreate, AuthUpdate
from .utils import hash_password


class AuthRepository(BaseRepository):

    def create(self, obj: AuthCreate) -> AuthSchema:
        query = """
        INSERT INTO auth (role, password, is_active, employee_id)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """

        return super()._excecute_query_with_result(
            query=query,
            variables=(
                obj.role,
                hash_password(obj.password),
                obj.is_active,
                obj.employee_id,
            ),
            schema=AuthSchema,
        )

    def get_by_id(self, obj_id: int) -> AuthSchema | None:
        query = "SELECT * FROM auth WHERE id = %s"

        return super()._excecute_query_with_result(
            query=query,
            variables=(obj_id,),
            schema=AuthSchema,
            commit=False,
        )

    def get_by_employee_email(self, email: str) -> AuthSchema | None:
        query = """
        SELECT auth.id, role, password, is_active, employee_id, email
        FROM auth 
        INNER JOIN public.employees e
        on e.id = auth.employee_id 
        WHERE email = %s
        """

        return super()._excecute_query_with_result(
            query=query,
            variables=(email,),
            schema=AuthSchema,
            commit=False,
        )

    def get_by_employee_phone(self, phone: str) -> AuthSchema | None:
        query = """
        SELECT auth.id, role, password, is_active, employee_id, phone
        FROM auth 
        INNER JOIN public.employees e
        on e.id = auth.employee_id
        WHERE phone = %s
        """

        return super()._excecute_query_with_result(
            query=query,
            variables=(phone,),
            schema=AuthSchema,
            commit=False,
        )

    def get_by_employee_id(self, obj_id: int) -> AuthSchema | None:
        query = "SELECT * FROM auth WHERE employee_id = %s"

        return super()._excecute_query_with_result(
            query=query,
            variables=(obj_id,),
            schema=AuthSchema,
            commit=False,
        )

    def get_all(self, page: int, page_size: int) -> list[AuthSchema]:
        raise NotImplementedError

    def update_by_id(self, obj_id: int, obj_update: Any) -> Any:
        raise NotImplementedError

    def update_by_employee_id(self, obj_id: int, obj_update: AuthUpdate) -> AuthSchema:
        return super()._update_by_id(
            table_name="auth",
            obj_id=obj_id,
            obj_update=obj_update,
            schema=AuthSchema,
            id_field="employee_id",
        )

    def update_password_by_employee_id(self, obj_id: int, password: str) -> AuthSchema:
        query = """
        UPDATE auth 
        SET password = %s
        WHERE employee_id = %s 
        RETURNING *
        """

        return super()._excecute_query_with_result(
            query=query,
            variables=(
                hash_password(password),
                obj_id,
            ),
            schema=AuthSchema,
        )

    def delete_by_id(self, obj_id: int) -> None:
        raise NotImplementedError

    def delete_by_employee_id(self, obj_id: int) -> None:
        query = "DELETE FROM auth WHERE employee_id = %s"

        super()._excecute_query(query, (obj_id,))
