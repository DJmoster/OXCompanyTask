import re
from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, model_validator, field_validator

from app.config import settings

from .enums import LoginType, AuthRole


class AuthCreate(BaseModel):
    role: AuthRole = AuthRole.USER
    password: str
    is_active: bool = True
    employee_id: int

    class Config:
        from_attributes = True


class AuthCreateResponse(AuthCreate):
    id: int


class AuthUpdate(BaseModel):
    role: Optional[AuthRole] = None
    is_active: Optional[bool] = None


class AuthUpdateResponse(AuthUpdate):
    role: AuthRole
    is_active: bool
    employee_id: int


class AuthSchema(AuthCreateResponse):
    password: bytes

    @field_validator("password", mode="before")
    def validate_password(cls, value):
        if isinstance(value, memoryview):
            value = value.tobytes()
        return value


class LoginUser(BaseModel):
    login: Annotated[str, MaxLen(50)]
    password: Annotated[str, MinLen(8), MaxLen(50)]

    _login_type: LoginType = LoginType.EMAIL

    @property
    def login_type(self) -> LoginType:
        return self._login_type

    @login_type.setter
    def login_type(self, login_type: LoginType):
        self._login_type = login_type

    @model_validator(mode="after")
    def set_login_type(cls, instance):
        if re.fullmatch(settings.validation.email_pattern, instance.login):
            instance.login_type = LoginType.EMAIL

        elif re.fullmatch(settings.validation.phone_pattern, instance.login):
            instance.login_type = LoginType.PHONE
        else:
            raise ValueError("Login field is not an email or phone number")

        return instance

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = settings.token.type
