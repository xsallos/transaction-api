__all__ = ("settings", "Settings")

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    stage: str = Field(alias="STAGE")  # one of: tests, development, qa, production
    # api_key: str = Field(alias="API_KEY")

    db_hostname: str = Field(alias="DB_HOSTNAME")
    db_name: str = Field(alias="DB_NAME")
    db_port: str = Field(alias="DB_PORT")
    db_username: str = Field(alias="DB_USERNAME")
    db_password: str = Field(alias="DB_PASSWORD")


settings = Settings()
