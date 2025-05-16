from langchain_openai import ChatOpenAI
from project_config import get_project_config
from functools import lru_cache
from log_manager import logger
config=get_project_config()

@lru_cache
def get_llm():
    try:
        LLM = ChatOpenAI(model="gpt-4-turbo", openai_api_key=config.OPENAI_API_KEY, temperature=0,verbose=True)
        logger.debug("ChatOpenAI instance created successfully")
    except Exception as exe:
        logger.error(f"Error initializing ChatOpenAI: {exe}", exc_info=True)
        raise RuntimeError(f"Initialization failed for ChatOpenAI due to: {exe}")
    return LLM
