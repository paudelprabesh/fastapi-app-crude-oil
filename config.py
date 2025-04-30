from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Crude oil import API"
    DATABASE_URL: str = (
        "postgresql+asyncpg://user:pass@localhost:5432/crude_oil_db"
    )


settings = Settings()
