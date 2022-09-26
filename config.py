from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    MYSQL_HOST: str = Field(env='MYSQL_HOST', default='localhost')
    MYSQL_USER: str = Field(env='MYSQL_USER', default='root')
    MYSQL_PASSWORD: str = Field(env='MYSQL_PASSWORD', default='12345678')
    MYSQL_PORT = Field(env='MYSQL_PORT', default=3306)
    MYSQL_DB = Field(env='MYSQL_DB', default='chat')
    LOG_LEVEL: str = Field(env='LOG_LEVEL', default='INFO')
    ENCODER: str = Field(env='ENCODER', default='utf-8')


settings = Settings()
