import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import logging


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')  # type: ignore
    TAVILY_API_KEY: str = Field(..., env='TAVILY_API_KEY')  # type: ignore
    GOOGLE_PLACES_API_KEY: str = Field(..., env='GOOGLE_PLACES_API_KEY')  # type: ignore
    LANGCHAIN_TRACING_V2: str = Field(..., env='LANGCHAIN_TRACING_V2') # type: ignore
    LANGCHAIN_ENDPOINT: str = Field(..., env='LANGCHAIN_ENDPOINT') # type: ignore
    LANGCHAIN_API_KEY: str = Field(..., env='LANGCHAIN_API_KEY') # type: ignore
    LANGCHAIN_PROJECT: str = Field(..., env='LANGCHAIN_PROJECT') # type: ignore
    MAX_TRIM_TOKENS: int = Field(1024, env='MAX_TRIM_TOKENS')  # type: ignore
    class Config:
        env_file = '.env'  # Specify the .env file

@lru_cache
def get_project_config() -> Settings:
    try:
        settings = Settings()  # type: ignore
        logging.debug("Settings successfully loaded.")
        return settings
    except Exception as exe:
        logging.error(f"Error loading settings: {exe}", exc_info=True)
        raise