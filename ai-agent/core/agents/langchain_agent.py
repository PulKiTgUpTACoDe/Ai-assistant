import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from core.tools.langchain_tools import tools
from core.tools.web_tools import web_tools
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.7
)

langgraph_agent = create_react_agent(llm, tools)
langgraph_web_agent = create_react_agent(llm, web_tools)