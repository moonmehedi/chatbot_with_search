#Step1: Setup Pydantic Model (Schema Validation)

from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt:str
    messages: List[str]
    allow_search: bool



#Step2: Stepup AiAgent according frontend request
from fastapi import FastAPI, HTTPException
from ai_agent import get_response_from_ai_agent

app = FastAPI(title="LANGGraph AI AGENT")


ALLOWED_MODEL_NAMES=['gpt-4o-mini','deepseek-r1-distill-llama-70b','llama-3.3-70b-versatile']

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """"
    API endpoint to handle chat and search requests .
    It dynamically selects the model specified in the request

    """


    if request.model_name not in ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Model not allowed")
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    prompt = request.system_prompt
    provider = request.model_provider
    

    response=get_response_from_ai_agent(llm_id,query,allow_search,prompt,provider)
    return response


# Step3: Run the app and Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)