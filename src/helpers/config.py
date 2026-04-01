from pydantic_settings import BaseSettings  # we use pydantic-settings to manage our configuration settings, which allows us to easily load environment variables and validate them

class settings(BaseSettings):
    
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE_MB: int
    FILE_DEFULT_CHUNK_SIZE: int

    class Config:                     # nested class to specify configuration for the settings
        env_file = ".env"


def get_settings():    # function to create an instance of the settings class, which will load the environment variables and return the settings object
    return settings()
