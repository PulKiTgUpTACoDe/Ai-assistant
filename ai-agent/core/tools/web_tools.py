from langchain.tools import tool
from typing import Any, Optional, List
from .news_api import NewsAPIWrapper
from .image_recognition import analyze_image
from langchain_community.utilities import (
    SerpAPIWrapper,
    WolframAlphaAPIWrapper,
    WikipediaAPIWrapper,
)
from .image_generation import generate_image
from .document_reader import answer_question, ingest_documents

@tool
def google_search(query: str) -> dict:
    """Searches Google (via Serper API) for the provided query or topic."""
    try:
        search = SerpAPIWrapper()
        result = search.run(query)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def wikipedia(query: str) -> Any:
    """Searches Wikipedia for the provided query or topic."""
    try:
        search = WikipediaAPIWrapper()
        result = search.load(query)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
    
@tool
def math_calc(query: str) -> dict:
    """Solve complex math, science, and computational problems. Input should be a precise question."""
    wolfram_client = WolframAlphaAPIWrapper()
    result = wolfram_client.run(query)
    return {'result': result}

@tool
def get_news(
    query: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_by: str = "relevancy",
    limit: int = 5
) -> dict:
    """This tool gives a thorough news and information about any topic that is asked. Use this when asked about current events or news.

    Args:
        query: Search keywords (e.g. "artificial intelligence")
        from_date: Optional start date in YYYY-MM-DD format
        to_date: Optional end date in YYYY-MM-DD format
        sort_by: One of 'relevancy', 'popularity', or 'publishedAt'
        limit: Number of articles to return (1-10) """

    news = NewsAPIWrapper()
    try:
        articles = news.search_news(
            query=query,
            from_date=from_date,
            to_date=to_date,
            sort_by=sort_by,
            page_size=min(max(limit, 1), 10)
        )
        
        if not articles or "error" in articles[0]:
            return "No news articles found"
            
        formatted_articles = []
        for article in articles[:limit]:
            formatted = f"Title: {article['title']}\nSource: {article['source']}\nPublished: {article['published_at']}\nSummary: {article['description']}\nURL: {article['url']}"
            formatted_articles.append(formatted)
            
        return {"result": f"Latest news about {query}:\n\n" + "\n\n".join(formatted_articles)}
        
    except Exception as e:
        return {"error": f"Error fetching news: {str(e)}"}

@tool
def recall_context(query: str) -> dict:
    """Recall relevant information from previous conversations when user refers to past discussions."""
    from core.memory.chat_history import ChatHistory
    chat_history_manager = ChatHistory()
    return chat_history_manager.get_relevant_context(query, k=3)

@tool
def image_recognition(query: str) -> dict:
    """Analyzes images provided by the user to provide descriptions and identify objects."""
    response = analyze_image(query)
    return response

@tool
def image_generation(prompt: str, name: str, output_format: str = "jpeg", negative_prompt: str = None, aspect_ratio: str = None, mode: str = "text-to-image", seed: int = None, strength: float = None, image: str = None, **kwargs) -> dict:
    """Generates an image from a text prompt using the Stability API."""
    try:
        image_path = generate_image(
            prompt=prompt,
            name=name,
            output_format=output_format,
            negative_prompt=negative_prompt,
            aspect_ratio=aspect_ratio,
            mode=mode,
            seed=seed,
            strength=strength,
            image=image,
            **kwargs
        )
        return {"result": f"Image generated and saved to {image_path}"}
    except Exception as e:
        return {"error": str(e)}

@tool
def ask_document_question(question: str) -> dict:
    """Answers a question by searching all ingested documents using RAG and Gemini LLM."""
    try:
        answer = answer_question(question)
        return {"result": answer}
    except Exception as e:
        return {"error": str(e)}

@tool
def web_automation(url: Optional[str], task: str = "extract all content") -> dict:
    """Performs web automation tasks using browser automation and AI-powered interaction."""
    from .ai_scraper import web_automation_task
    import asyncio
    try:
        result = asyncio.run(web_automation_task(url, task))
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# List of web-safe tools
web_tools = [
    google_search,
    wikipedia,
    math_calc,
    get_news,
    recall_context,
    image_recognition,
    image_generation,
    ask_document_question,
    web_automation,
] 