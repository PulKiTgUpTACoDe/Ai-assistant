from langchain.tools import tool
import datetime
import webbrowser
import time
import pyautogui

@tool
def open_app(app_name: str):
    """Opens a desktop or web application based on the provided app name."""
    try:
        pyautogui.press('win')
        time.sleep(0.1)
        pyautogui.write(app_name)
        time.sleep(0.1)
        pyautogui.press('enter')
        return {"result": f"Successfully opened {app_name}"}
    except Exception as e:
        return {"result": f"Failed to open {app_name}: {str(e)}"}

@tool
def search_google(query: str):
    """Searches Google for the provided query or topic."""
    try:
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return {"result": f"Searching Google for {query}"}
    except Exception as e:
        return {"result": f"Search failed: {str(e)}"}

@tool
def play_music(song_name: str):
    """Plays the specified song using an online music player. Use this when the user requests to play music."""
    from core.tools import audio_player
    try:
        audio_player.play_music(song_name)
        return {"result": f"Now playing {song_name}"}
    except Exception as e:
        return {"result": f"Failed to play music: {str(e)}"}

@tool
def get_current_time() -> str:
    """Returns the current system time."""
    try:
        return {"result": datetime.datetime.now().strftime("%H:%M")}
    except Exception as e:
        return {"result": f"Failed to get time: {str(e)}"}

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
        chat_history_manager = chat_history.ChatHistory(session_only=True)
        chat_history_manager.end_session()
        sys.exit()
        return {"result": "Goodbye!"}
    except Exception as e:
        return {"result": f"Exit failed: {str(e)}"}

tools = [
    open_app, search_google, play_music, get_current_time,
    screenshot, weather, shutdown, restart,
    set_volume, increase_volume, decrease_volume, exit
]