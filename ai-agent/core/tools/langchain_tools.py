from langchain.tools import tool
import datetime
import time
import pyautogui
from dotenv import load_dotenv
from typing import Any, Optional, List
from .news_api import NewsAPIWrapper
from .object_detection import analyze_visual_input
from .image_recognition import analyze_image
from .whatsapp_automation import get_message_for_whatsapp
from langchain_community.utilities import (
    SerpAPIWrapper,
    WolframAlphaAPIWrapper,
    WikipediaAPIWrapper,
)
from .image_generation import generate_image
from .document_reader import answer_question, ingest_documents, load_documents_from_folder

load_dotenv()

@tool
def open_app(app_name: str):
    """Opens a desktop or web application based on the provided app name."""
    try:
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(0.5)
        pyautogui.press('enter')
        return {"result": f"Successfully opened {app_name}"}
    except Exception as e:
        return {"result": f"Failed to open {app_name}: {str(e)}"}

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
    """Searches Wkipedia for the provided query or topic."""
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
    return {'result':result}

@tool
def send_whatsApp_message(query: str) -> dict:
    """Sends a message on whatsapp on the users request or if necessary
    The query would contain atleast the recipient's name/phone number to which the message is to be sent and the message content that has to be sent.
    """

    return get_message_for_whatsapp(query)

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
def play_music(song_name: str):
    """Plays the specified song using an online music player. Use this when the user requests to play music."""
    from core.tools import audio_player
    try:
        audio_player.play_music(song_name)
        return {"result": f"Now playing {song_name}"}
    except Exception as e:
        return {"result": f"Failed to play music: {str(e)}"}

# langchain_tools.py
@tool
def stop_music() -> dict:
    """Stops any currently playing music when user requests to stop. Use phrases like 'stop music', 'pause song', or 'I want to stop listening'."""
    from core.tools import audio_player
    return audio_player.stop_music()

@tool
def get_current_time() -> str:
    """Returns the current system time."""
    try:
        return {"result": datetime.datetime.now().strftime("%H:%M")}
    except Exception as e:
        return {"result": f"Failed to get time: {str(e)}"}

@tool
def recall_context(query: str) -> dict:
    """Recall relevant information from previous conversations when user refers to past discussions. Use phrases like 'remember when', 'as we discussed', etc. Whenever you feel that the user might be taking past conversation as its current referrence the use this tool.
    Use your reasoning to know when could a user refer past conversation and call this tool"""
    
    from core.memory.chat_history import ChatHistory
    chat_history_manager = ChatHistory()
    return chat_history_manager.get_relevant_context(query, k=3)

@tool
def object_detection_visual(query: str) -> dict:
    """Consider this your new eyes and analyzes the current scene from the camera feed to answer questions or describe what is seen.
    Use this tool when the user asks about their surroundings, what something looks like,
    or asks you about your vision.
    Provide a clear query asking specifically what information is needed from the image."""
    
    response = analyze_visual_input(query);
    return response

@tool
def image_recognition(query: str) -> dict:
    """Use this tool when the user says to see or analyse what's on his screen. Using this tool you can now see the screenshot on the screen and be able to provide descripion and analyse the image and objects on the screen.
    User can ask you same questions in which he wouldn't say to directly use this tool but you yourself have to understant the context of the query and use this tool to give appropriate answers.
    """
    
    response = analyze_image(query);
    return response

@tool
def shutdown():
    """Shuts down the system immediately."""
    from core.utils import system_commands
    try:
        system_commands.shutdown_system()
        return {"result": "System is shutting down..."}
    except Exception as e:
        return {"result": f"Shutdown failed: {str(e)}"}

@tool
def restart():
    """Restarts the system immediately."""
    from core.utils import system_commands
    try:
        system_commands.restart_system()
        return {"result": "System is restarting..."}
    except Exception as e:
        return {"result": f"Restart failed: {str(e)}"}

@tool
def screenshot():
    """Captures a screenshot of the current screen."""
    from core.utils import file_utils
    try:
        file_utils.take_screenshot()
        return {"result": "Screenshot taken successfully"}
    except Exception as e:
        return {"result": f"Screenshot failed: {str(e)}"}

@tool
def weather(city: str) -> str:
    """Fetches weather information for a specified city."""
    from core.utils.weather import get_weather
    try:
        result = get_weather(city)
        return {"result": result}
    except Exception as e:
        return {"result": f"Weather check failed: {str(e)}"}

@tool
def set_volume(level: int):
    """Sets the system volume to specified percentage (0-100)."""
    from core.utils import volume_control
    try:
        volume_control.set_volume(level)
        return {"result": f"Volume set to {level}%"}
    except Exception as e:
        return {"result": f"Volume adjustment failed: {str(e)}"}

@tool
def increase_volume():
    """Increases the system volume by 10%."""
    from core.utils import volume_control
    try:
        volume_control.increase_volume()
        return {"result": "Volume increased"}
    except Exception as e:
        return {"result": f"Volume increase failed: {str(e)}"}

@tool
def decrease_volume():
    """Decreases the system volume by 10%."""
    from core.utils import volume_control
    try:
        volume_control.decrease_volume()
        return {"result": "Volume decreased"}
    except Exception as e:
        return {"result": f"Volume decrease failed: {str(e)}"}

@tool
def exit():
    """Ends the chat session and exits the assistant."""
    try:
        import sys
        from core.memory import chat_history
        # chat_history_manager = chat_history.ChatHistory(session_only=True)
        # chat_history_manager.end_session()
        sys.exit()
    except Exception as e:
        return {"result": f"Exit failed: {str(e)}"}

@tool
def image_generation(prompt: str, name: str, output_format: str = "jpeg", negative_prompt: str = None, aspect_ratio: str = None, mode: str = "text-to-image", seed: int = None, strength: float = None, image: str = None, **kwargs) -> dict:
    """
    Generates an image from a text prompt using the Stability API with full control over all parameters. The AI can decide positive/negative prompts, aspect ratio, mode, seed, strength, and more. Decide all the input values for yourself or use default values until user dosen't specifies it explicitly. Don't ask again and again if user is not specifying.
    Args:
        prompt: Positive prompt for the image.
        name: Name for the generated image file, Decide it yourself according to the content of the image.
        output_format: Output format (jpeg, png, etc). Use default format until user describes.
        negative_prompt: What you do NOT want in the image. Decide it yourself until user dosen't specifies it or leave it.
        aspect_ratio: Aspect ratio (e.g., '16:9', '1:1', etc.) Decide it yourself based on the query.
        mode: 'text-to-image' or 'image-to-image'.
        seed: Random seed for reproducibility.
        strength: Denoising strength (for image-to-image).
        image: Base64-encoded image for image-to-image mode.
        **kwargs: Any additional API parameters.

        Returns:
            Path to the saved image file.
    """

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
def get_base64_image_from_public(filename: str) -> str:
    """
    Reads an image from ai-agent/public and returns its base64-encoded string.
    Use this tool when the user is asking to generate image using another image or its base-64 string.
    Use the output of this tool as the input of image_generation tool to use image to image generation

    Args:
        filename: The name of the image file.
    Returns:
        Base64-encoded string of the image.
    """
    import base64
    import os

    try:
        path = os.path.join("ai-agent", "public", filename)
        with open(path, "rb") as img_file:
            return {"result": f"Base64-encoded image is {base64.b64encode(img_file.read()).decode("utf-8")}"}
        
    except Exception as e:
        return {"error": str(e)}

@tool
def ask_document_question(question: str) -> dict:
    """Answers a question by searching all ingested documents (PDFs, text files) using RAG and Gemini LLM. Returns a synthesized answer with sources."""

    try:
        answer = answer_question(question)
        return {"result": answer}
    except Exception as e:
        return {"error": str(e)}

tools = [
    open_app, google_search, wikipedia, math_calc,play_music, stop_music, get_current_time, get_news, recall_context, send_whatsApp_message,
    screenshot, weather, object_detection_visual, image_recognition, shutdown, restart,
    set_volume, increase_volume, decrease_volume, exit, image_generation, get_base64_image_from_public, ask_document_question,
]