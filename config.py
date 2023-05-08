from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    database_name: str
    password: str
    username: str

    class Config:
        env_file = ".env"


settings = Settings()
