from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    DATABASE_URL: str = config("DATABASE_URL")
    DATABASE_NAME: str = config("DATABASE_NAME")

    PROJECT_NAME: str = config("PROJECT_NAME")
    API_V1_STR: str = config("API_V1_STR")

    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")

    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY")

    STRIPE_SECRET_KEY: str = config("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: str = config("STRIPE_PUBLISHABLE_KEY")
    STRIPE_WEBHOOK_SECRET: str = config("STRIPE_WEBHOOK_SECRET")
    FRONTEND_URL: str = config("FRONTEND_URL")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 999
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()
