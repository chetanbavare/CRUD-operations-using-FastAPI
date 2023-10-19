from pydantic_settings import BaseSettings
# using basesettings to configure environment variables, this is the schema

class Settings(BaseSettings):
    database_hostname : str
    database_port :str
    database_username : str
    database_password: str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int 

    class Config: # config file is env
        env_file = ".env"

settings = Settings() # settings object created will be used as variable 
