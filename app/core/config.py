from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env") #env_prefix can be used to attach a prefix for env name's while lookup

    environment: str = "Test"
    project_name: str = "Altruis-AG Drug Lookup"
    version: str = "1.0.1"
    echo_sql: bool = True
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str


settings = Settings()