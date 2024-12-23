from app.config import settings

from app.database.database import db_helper

from api_v1.employees.repository import EmployeeRepository
from api_v1.employees.schemas import EmployeeCreate
from app.api_v1.employees.enums import EmployeePosition

from api_v1.auth.repository import AuthRepository
from api_v1.auth.schemas import AuthCreate
from app.api_v1.auth.enums import AuthRole


class DatabaseUtils:
    @staticmethod
    def create_tables():
        with open(settings.db.schema_dir, "r") as schema_file:
            cursor = db_helper.cursor

            cursor.execute(schema_file.read())
            cursor.connection.commit()

            cursor.close()
            db_helper.pool.putconn(cursor.connection)

    @staticmethod
    def create_basic_admin():
        cursor = db_helper.cursor

        employee_repository = EmployeeRepository(cursor)
        auth_repository = AuthRepository(cursor)

        if not auth_repository.get_by_employee_email("admin@admin.com"):
            employee_record = employee_repository.create(
                EmployeeCreate(
                    first_name="Admin",
                    last_name="Admin",
                    email="admin@admin.com",
                    phone="+38099999999",
                    position=EmployeePosition.SOFTWARE_ENGINEER,
                )
            )

            auth_repository.create(
                AuthCreate(
                    role=AuthRole.ADMIN,
                    password="1234567890",
                    employee_id=employee_record.id,
                )
            )

        cursor.close()
        db_helper.pool.putconn(cursor.connection)
