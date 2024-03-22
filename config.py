from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    database_id: str
    openai_organization: str
    openai_api_key: str
    hf_token: str

    class Config:
        env_file = ".env"


settings = Settings()
