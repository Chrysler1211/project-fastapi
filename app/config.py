from pydantic_settings import BaseSettings, SettingsConfigDict



class setting(BaseSettings):

    DATABASE_HOSTNAME : str
    DATABASE_NAME : str
    DATABASE_USERNAME : str
    DATABASE_PORT : str
    DATABASE_PASSWORD : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

  
    model_config = SettingsConfigDict(env_file= ".env")


settings = setting()


