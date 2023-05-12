from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str
    database_id: str

    class Config:
        env_file = ".env"


settings = Settings()
