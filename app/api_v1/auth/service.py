from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

from app.base import Base

from .enums import LoginType
from .repository import AuthRepository
from .schemas import (
    LoginUser,
    TokenResponse,
    AuthCreate,
    AuthCreateResponse,
    AuthUpdate,
    AuthUpdateResponse,
)
from .utils import create_jwt_token, validate_password, generate_random_password
from .exceptions import (
    INVALID_EMAIL_OR_PASSWORD_EXCEPTION,
    USER_NOT_ACTIVE_EXCEPTION,
    USER_CREDENTIALS_ALREARY_CREATED_EXCEPTION,
    USER_NOT_FOUND_EXCEPTION,
)


class AuthService(Base):
    def __init__(self, cursor: RealDictCursor):
        super().__init__(cursor)

        self.__auth_repository = AuthRepository(cursor)

    async def login_user(self, user: LoginUser) -> TokenResponse:
        auth_record = None
        match user.login_type:
            case LoginType.EMAIL:
                auth_record = self.__auth_repository.get_by_employee_email(user.login)
            case LoginType.PHONE:
                auth_record = self.__auth_repository.get_by_employee_phone(user.login)

        if auth_record is None or not validate_password(
            user.password, auth_record.password
        ):
            raise INVALID_EMAIL_OR_PASSWORD_EXCEPTION

        if not auth_record.is_active:
            raise USER_NOT_ACTIVE_EXCEPTION

        return create_jwt_token(auth_record.id, auth_record.role)

    async def create(self, employee_id: int, auth_in: AuthUpdate) -> AuthCreateResponse:
        password = generate_random_password()
        try:
            auth_record = self.__auth_repository.create(
                AuthCreate(
                    role=auth_in.role,
                    is_active=auth_in.is_active,
                    password=password,
                    employee_id=employee_id,
                )
            )
        except UniqueViolation:
            raise USER_CREDENTIALS_ALREARY_CREATED_EXCEPTION
        except ForeignKeyViolation:
            raise USER_NOT_FOUND_EXCEPTION

        return AuthCreateResponse.model_validate(
            {
                "password": password,
                **auth_record.model_dump(exclude=("password",)),
            }
        )

    async def get_by_employee_id(self, employee_id: int) -> AuthUpdateResponse:
        auth_record = self.__auth_repository.get_by_employee_id(employee_id)

        if auth_record is None:
            raise USER_NOT_FOUND_EXCEPTION

        return AuthUpdateResponse.model_validate(auth_record.model_dump())

    async def update_by_employee_id(
        self, employee_id: int, obj_update: AuthUpdate
    ) -> AuthUpdateResponse:
        auth_record = self.__auth_repository.update_by_employee_id(
            employee_id, obj_update
        )

        if auth_record is None:
            raise USER_NOT_FOUND_EXCEPTION

        return AuthUpdateResponse.model_validate(auth_record.model_dump())

    async def delete_by_employee_id(self, employee_id: int) -> None:
        self.__auth_repository.delete_by_employee_id(employee_id)
