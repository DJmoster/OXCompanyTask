from app.base import BaseRepository

from .schemas import EmployeeSchema, EmployeeCreate, EmployeeUpdate


class EmployeeRepository(BaseRepository):
    def create(self, obj: EmployeeCreate) -> EmployeeSchema:
        query = """
        INSERT INTO employees (first_name, last_name, email, phone, position)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """

        return super()._excecute_query_with_result(
            query=query,
            variables=(
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.phone,
                obj.position,
            ),
            schema=EmployeeSchema,
        )

    def get_by_id(self, obj_id: int) -> EmployeeSchema | None:
        query = "SELECT * FROM employees WHERE id = %s"

        return super()._excecute_query_with_result(
            query=query,
            variables=(obj_id,),
            schema=EmployeeSchema,
            commit=False,
        )

    def get_all(self, page: int, page_size: int) -> list[EmployeeSchema]:
        query = """
        SELECT * FROM employees
        ORDER BY id
        LIMIT %s OFFSET %s;
        """
        offset = (page - 1) * page_size

        self._cursor.execute(query, (page_size, offset))

        return [
            EmployeeSchema.model_validate(dict(res)) for res in self._cursor.fetchall()
        ]

    def update_by_id(
        self, obj_id: int, obj_update: EmployeeUpdate
    ) -> EmployeeSchema | None:
        return super()._update_by_id(
            table_name="employees",
            obj_id=obj_id,
            obj_update=obj_update,
            schema=EmployeeSchema,
        )

    def delete_by_id(self, obj_id: int) -> None:
        query = "DELETE FROM employees WHERE id = %s"

        super()._excecute_query(query, (obj_id,))
