from functools import wraps

from .enums import AuthRole
from .schemas import AuthSchema
from .exceptions import USER_NOT_PERMITTED_EXCEPTION


def role_requiered(roles: list[AuthRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: AuthSchema = kwargs.get("current_user")

            if current_user is None:
                raise ValueError("Current user not found")

            if current_user.role not in roles:
                raise USER_NOT_PERMITTED_EXCEPTION

            return await func(*args, **kwargs)

        return wrapper

    return decorator
