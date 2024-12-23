from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class DataBaseSettings(BaseModel):
    host: str = getenv("DB_HOST")
    name: str = getenv("DB_NAME")
    user: str = getenv("DB_USER")
    password: str = getenv("DB_PASSWORD")
    schema_filename: str = "schema.sql"


class TokenSettings(BaseModel):
    secret_key: str = getenv("TOKEN_SECRET_KEY")
    algorithm: str = "HS256"
    hash_encoding: str = "UTF-8"
    type: str = "Bearer"
    session_expire_minutes: int = int(getenv("TOKEN_EXPIRE_MINUTES", 120))


class ValidationSettings(BaseModel):
    email_pattern: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    phone_pattern: str = (
        r"^(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,3}?\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$"
    )


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DataBaseSettings = DataBaseSettings()
    token: TokenSettings = TokenSettings()
    validation: ValidationSettings = ValidationSettings()


settings = Settings()
