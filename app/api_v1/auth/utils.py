import bcrypt
import jwt
import string
import random

from datetime import timedelta, datetime

from app.config import settings

from .schemas import TokenResponse
from .enums import AuthRole


def create_jwt_token(auth_id: int, auth_role: AuthRole) -> TokenResponse:
    return TokenResponse(
        access_token=encode_jwt({"sub": auth_id, "role": auth_role.value}),
    )


def encode_jwt(
    payload: dict,
    secret_key: str = settings.token.secret_key,
    algorithm: str = settings.token.algorithm,
    expire_minutes: int = settings.token.session_expire_minutes,
):
    to_encode = payload.copy()
    to_encode.update(iat=datetime.utcnow())
    to_encode.update(exp=datetime.utcnow() + timedelta(minutes=expire_minutes))

    return jwt.encode(to_encode, secret_key, algorithm)


def decode_jwt(
    token: str,
    secret_key: str = settings.token.secret_key,
    algorithm: str = settings.token.algorithm,
):
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(settings.token.hash_encoding),
        bcrypt.gensalt(),
    )


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(settings.token.hash_encoding),
        hashed_password,
    )


def generate_random_password(length: int = 15) -> str:
    password = random.choices(string.ascii_letters + string.digits, k=length)
    random.shuffle(password)

    return "".join(password)
