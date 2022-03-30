from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    WEBHOOK_HOST: str
    WEBHOOK_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
