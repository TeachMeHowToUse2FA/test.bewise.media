from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Media Conversion Service"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    STORAGE_DIR: str = "storage"

    class Config:
        env_file = ".env"


settings = Settings()
