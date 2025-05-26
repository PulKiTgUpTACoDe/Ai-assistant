from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, BrowserProfile, Controller
from dotenv import load_dotenv
from typing import Any

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

browser_profile = BrowserProfile(
    executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    headless=False,
    args=[
        '--disable-gpu',
        '--no-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials'
    ]
)

browser_session = BrowserSession(
    browser_profile=browser_profile,
)

async def scrape_webpage(url: str, task: str = "extract all content") -> Any:
    """
    Scrape a webpage using browser-use Agent and Gemini LLM, returning structured data.
    Args:
        url: The URL of the webpage to scrape.
        task: The scraping task description.
    Returns:
        Raw content from the webpage.
    """
    try:
        agent = Agent(
            task=f"{task} from {url}",
            llm=llm,
            browser_session=browser_session,
        )

        raw_agent_output = await agent.run()
        result = raw_agent_output.final_result()
        return result

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
