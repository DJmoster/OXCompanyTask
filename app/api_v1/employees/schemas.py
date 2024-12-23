import re
from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, field_validator

from app.config import settings

from .enums import EmployeePosition


class EmployeeCreate(BaseModel):
    first_name: Annotated[str, MinLen(3), MaxLen(50)]
    last_name: Annotated[str, MinLen(3), MaxLen(50)]
    email: Annotated[EmailStr, MaxLen(50)]
    phone: Annotated[str, MinLen(9), MaxLen(15)]
    position: EmployeePosition

    @field_validator("phone", mode="after")
    def validate_phone(cls, value):
        if re.fullmatch(settings.validation.phone_pattern, value):
            return value
        else:
            raise ValueError("Invalid phone number")

    class Config:
        from_attributes = True


class EmployeeUpdate(EmployeeCreate):
    first_name: Annotated[Optional[str], MinLen(3), MaxLen(50)] = None
    last_name: Annotated[Optional[str], MinLen(3), MaxLen(50)] = None
    email: Annotated[Optional[EmailStr], MaxLen(50)] = None
    phone: Annotated[Optional[str], MinLen(9), MaxLen(15)] = None
    position: Optional[EmployeePosition] = None


class EmployeeSchema(EmployeeCreate):
    id: int


class EmployeeWithPasswordSchema(EmployeeSchema):
    password: str = None
