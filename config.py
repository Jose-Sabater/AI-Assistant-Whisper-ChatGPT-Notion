from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str
    database_id: str
    openai_organization: str
    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
