from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os
import yaml
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from project_config import get_project_config
from llm import get_llm
from log_manager import logging

# Initialize FastAPI
app = FastAPI()

# Load config and set API keys
config = get_project_config()
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY
print(config.TAVILY_API_KEY)

# Load LLM
LLM = get_llm()

# Load prompts
PROMPTS_PATH = Path("prompts.yaml")
with open(PROMPTS_PATH, "r", encoding="utf-8") as file:
    ALL_PROMPTS = yaml.safe_load(file)

# Pydantic model for request
class QueryRequest(BaseModel):
    user_question: str

# Function to classify query
def classify_query_with_router(user_question: str) -> str:
    system_prompt = SystemMessage(content=ALL_PROMPTS["router_system_prompt"])
    human_prompt = HumanMessage(content=user_question)
    result = LLM.invoke([system_prompt, human_prompt])
    return result.content.strip().lower() if isinstance(result, AIMessage) else ""

# Function to generate final response
def generate_response(user_question: str, search_results: list[str]) -> str:
    system_prompt = SystemMessage(content=ALL_PROMPTS["system_prompt"])
    human_prompt = HumanMessage(
        content=ALL_PROMPTS["human_prompt_template"].format(
            user_question=user_question,
            search_results="\n".join(search_results)
        )
    )
    result = LLM.invoke([system_prompt, human_prompt])
    return result.content if isinstance(result, AIMessage) else str(result)

# API endpoint
@app.post("/ask")
def ask_question(payload: QueryRequest):
    user_question = payload.user_question
    classification = classify_query_with_router(user_question)
    
    if classification == "restaurant":
        try:
            logging.info("Flow came into Restaurant Related Queries.")
            tavily = TavilySearchResults()
            search_response = tavily.invoke({"query": user_question, "num_results": 10})

            logging.info("Search response:", search_response)

            if isinstance(search_response, dict) and "results" in search_response:
                results_texts = [res["content"] for res in search_response["results"]]
            else:
                results_texts = [str(search_response)]

            response = generate_response(user_question, results_texts)
            return {"response": response}
        except Exception as e:
            print("Error during restaurant flow:", str(e))
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="The question is irrelevant. Please ask questions related to restaurants.")