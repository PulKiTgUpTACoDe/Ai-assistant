import threading
from core.audio import speech_recognition, text_to_speech, audio_player
# from core.NLP import dialogue_manager
from core.utils import system_commands, internet_utils, file_utils, volume_control, weather
from core.AI import gemini_ai, chat_history
from config import config
import re
import sys 

# Initialize components
speech_queue = text_to_speech.speech_queue
control_queue = text_to_speech.control_queue
gemini = gemini_ai.GeminiAI(api_key=config.GEMINI_API_KEY)
chat_history_manager = chat_history.ChatHistory()
music_playing = False # Global music state.

def handle_command(query):
    global music_playing

    if re.match(r'(open)\s+', query, re.IGNORECASE):
        app_name = re.sub(r'(open)\s*', '', query, flags=re.IGNORECASE).strip()
        if internet_utils.find_and_open_app(app_name):
            text_to_speech.say(f"Opening {app_name}...")
        else:
            text_to_speech.say("Some error occurred opening the app.")

    elif "search for" in query or "search" in query:
        app_name = re.sub(r'(search for|search)\s*', '', query, flags=re.IGNORECASE).strip()
        text_to_speech.say(f"Searching for {app_name}...")
        internet_utils.search_google(app_name)

    elif "play" in query:
        song_name = query.replace("play", "").strip()
        if song_name:
            audio_player.play_online_music(song_name)
            music_playing = True
        else:
            text_to_speech.say("Please specify a song name.")

    elif "the time" in query:
        text_to_speech.say(f"Sir, the time is {system_commands.get_time()}")

    elif "reset chat" in query or "clear history" in query:
        chat_history_manager.reset_history()
        text_to_speech.say("Chat history has been reset.")

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
        text_to_speech.say("Goodbye sir!")
        sys.exit()

    else:
        # Handle natural language queries
        response, lang = gemini.chat(query, chat_history_manager.get_history())
        chat_history_manager.add_message(query, response)

        # Speak and print the response
        text_to_speech.say(response, lang)


if __name__ == '__main__':
    print('\nWelcome to AI Assistant')

    # Start speech processing thread
    speech_thread = threading.Thread(target=text_to_speech.process_speech_queue, daemon=True)
    speech_thread.start()

    # Initial activation message
    text_to_speech.say("AI assistant is now active.")

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
        