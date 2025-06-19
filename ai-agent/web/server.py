from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Add the parent directory to Python path to import from ai-agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.langchain_agent import langgraph_web_agent


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Start with system message
        messages = [
            ("system", "You are an advanced AI assistant designed to help users with a wide range of tasks and tools. You can execute various tools in parallel or in order to give the most precise output the user would need."
            "I want you to not use asterisks signs in your answers strictly"
            "Your goal is to assist users efficiently, provide accurate information, and execute tasks seamlessly. Always prioritize user safety and confirm before performing critical actions like shutting down or restarting the system.")
        ]
        # Add context messages if available
        if request.context:
            for msg in request.context:
                if msg["role"] == "user":
                    messages.append(("user", msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(("tool", msg["content"]))
        # Add current message
        messages.append(("user", request.message))
        
        result = langgraph_web_agent.invoke({"messages": messages})

        ai_message = result["messages"][-1].content

        return ChatResponse(response=ai_message)
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 