from enum import Enum


class LoginType(int, Enum):
    EMAIL = 1
    PHONE = 2


class AuthRole(str, Enum):
    ADMIN = "Admin"
    MODERATOR = "Moderator"
    USER = "User"
