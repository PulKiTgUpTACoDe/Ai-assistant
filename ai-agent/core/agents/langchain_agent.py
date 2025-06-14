import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from core.tools.langchain_tools import tools
from core.tools.web_tools import web_tools
from langchain_core.utils.function_calling import convert_to_openai_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.7
)

# Convert tools to proper format
formatted_tools = [convert_to_openai_tool(t) for t in tools]
formatted_web_tools = [convert_to_openai_tool(t) for t in web_tools]

llm_with_tools = llm.bind_tools(formatted_tools)
llm_with_web_tools = llm.bind_tools(formatted_web_tools)