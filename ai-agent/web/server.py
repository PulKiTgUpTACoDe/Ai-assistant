from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to Python path to import from ai-agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.langchain_agent import llm, llm_with_web_tools
from core.tools.web_tools import web_tools

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

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

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = [
            SystemMessage(
                content="You are an advanced AI assistant designed to help users with a wide range of tasks and tools. You can execute various tools in parallel or in order to give the most precise output the user would need."
                "Your goal is to assist users efficiently, provide accurate information, and execute tasks seamlessly. Always prioritize user safety and confirm before performing critical actions like shutting down or restarting the system."
            ),
            HumanMessage(content=request.message)
        ]
        
        first_response = llm_with_web_tools.invoke(messages)
        
        if hasattr(first_response, 'tool_calls') and first_response.tool_calls:
            tool_responses = []
            for tool_call in first_response.tool_calls:
                tool = next((t for t in web_tools if t.name == tool_call['name']), None)
                if tool:
                    result = tool.invoke(tool_call['args'])
                    tool_responses.append(ToolMessage(
                        content=str(result['result']),
                        tool_call_id=tool_call['id']
                    ))
            
            # Generate final response after all tool calls
            if tool_responses:
                final_response = llm.invoke(messages + [first_response] + tool_responses)
                return ChatResponse(response=final_response.content)
            return ChatResponse(response=first_response.content)
        else:
            return ChatResponse(response=first_response.content)
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 