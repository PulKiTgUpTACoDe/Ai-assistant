import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from core.tools.langchain_tools import tools
from langchain_core.utils.function_calling import convert_to_openai_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    model="gemini-2.0-flash",
    temperature=0.7
)

# try:
#     llm = ChatDeepSeek(
#         model="deepseek-chat",
#         api_key=os.getenv("DEEPSEEK_API_KEY"),
#         base_url="https://api.deepseek.com",
#         temperature=0.7,
#         max_tokens=2048
#     )
# except Exception as e:
#     print(f"Error initializing ChatOpenAI: {e}")

# Convert tools to proper format
formatted_tools = [convert_to_openai_tool(t) for t in tools]

llm_with_tools = llm.bind_tools(formatted_tools)