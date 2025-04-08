import threading
import re
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core components
from core.tools import speech_recognition, speech_synthesis, audio_player
from core.utils import system_commands, internet_utils, file_utils, volume_control, weather
from core.agents import ai_chatBot
from core.memory import chat_history

# Initialize components
speech_queue = speech_synthesis.speech_queue
control_queue = speech_synthesis.control_queue
ai_chat = ai_chatBot.ChatBot(api_key=os.getenv("GEMINI_API_KEY"))
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False

def handle_command(query):
    global music_playing

    if re.match(r'(open)\s+', query, re.IGNORECASE):
        app_name = re.sub(r'(open)\s*', '', query, flags=re.IGNORECASE).strip()
        if internet_utils.find_and_open_app(app_name):
            speech_synthesis.say(f"Opening {app_name}...")
        else:
            speech_synthesis.say("Some error occurred opening the app.")

    elif "search for" in query or "search" in query:
        app_name = re.sub(r'(search for|search)\s*', '', query, flags=re.IGNORECASE).strip()
        speech_synthesis.say(f"Searching for {app_name}...")
        internet_utils.search_google(app_name)

    elif "play" in query:
        song_name = query.replace("play", "").strip()
        if song_name:
            audio_player.play_online_music(song_name)
            music_playing = True
        else:
            speech_synthesis.say("Please specify a song name.")

    elif "the time" in query:
        speech_synthesis.say(f"Sir, the time is {system_commands.get_time()}")

    elif "reset chat" in query or "clear history" in query:
        chat_history_manager.reset_history()
        speech_synthesis.say("Chat history has been reset.")

    elif "take screenshot" in query:
        file_utils.take_screenshot()

    elif "weather" in query:
        city = re.search(r'\b(?:weather\s*in)\s+([a-zA-Z\s]+)', query, re.IGNORECASE).group(1).strip()
        weather.get_weather(city)

    elif "shutdown" in query:
        system_commands.shutdown_system()

    elif "restart" in query:
        system_commands.restart_system()

    elif "set volume to" in query:
        volume_level = int(re.search(r'set volume to (\d+)', query).group(1))
        volume_control.set_volume(volume_level)

    elif "increase volume" in query:
        volume_control.increase_volume()

    elif "decrease volume" in query:
        volume_control.decrease_volume()

    elif "exit" in query:
        speech_synthesis.say("Goodbye sir!")
        
        sys.exit()

    else:
        # Get relevant context from vector memory
        relevant_context = chat_history_manager.get_relevant_context(query)
        
        # Get recent chat history (last 10 messages)
        recent_history = chat_history_manager.get_history(max_messages=10)
        
        # Combine recent history with relevant context from vector memory
        if relevant_context:
            combined_context = f"{relevant_context}\n\nRecent conversation:\n{recent_history}"
        else:
            combined_context = recent_history
        
        # Handle natural language queries with enhanced context
        response, lang = ai_chat.chat(query, combined_context)
        chat_history_manager.add_message(query, response)

        # Speak and print the response
        speech_synthesis.say(response, lang)


if __name__ == '__main__':
    print('\nWelcome to AI Assistant')

    # Start speech processing thread
    speech_thread = threading.Thread(target=speech_synthesis.process_speech_queue, daemon=True)
    speech_thread.start()

    # Initial activation message
    speech_synthesis.say("AI assistant is now active.")

    try:
        while True:
            query = speech_recognition.takeCommand()
            if query and not music_playing:
                handle_command(query)
            elif music_playing and query:
                if "stop" in query:
                    audio_player.stop_music()
                    music_playing = False
            else:
                continue
    except KeyboardInterrupt:
        print("\nShutting down...")
        chat_history_manager.end_session()
    except Exception as e:
        print(f"\nError: {e}")
        chat_history_manager.end_session()
        