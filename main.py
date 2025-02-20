import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
import sys
import threading
import queue
import yt_dlp
import vlc
import requests
import pyautogui
import re
from langdetect import detect
from googletrans import Translator
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google import genai
from config import apikey, wheatherAPI

# Initialize GEMINI AI client
GEMINI_API_KEY = apikey
client = genai.Client(api_key=GEMINI_API_KEY)

# Text-to-Speech setup moved to the processing thread
speech_queue = queue.Queue()
control_queue = queue.Queue()

# Global variables
translator = Translator()
chatStr = ""
speaking = False  # Track if AI is speaking
player = None

def stop_speaking():
    control_queue.put("stop")

def say(text, lang="en"):
    global speaking
    speaking = True

    # Preserve code blocks in English
    if "```" in text:
        print(f"\n{text}\n")
        speech_queue.put((text, "en"))
        return

    print(f"\nJarvis ({'Hindi' if lang == 'hi' else 'English'}): {text}")
    speech_queue.put((text, lang))

def process_speech_queue():
    # Processes speech requests in a dedicated thread
    engine = pyttsx3.init()
    
    # Get available voices and identify Hindi voice
    voices = engine.getProperty('voices')
    hindi_voice = None
    english_voice = None
    
    # Set Hindi and English voices
    hindi_voice = voices[1].id 
    english_voice = voices[0].id

    while True:
        try:
            cmd = control_queue.get_nowait()
            if cmd == "stop":
                engine.stop()
        except queue.Empty:
            pass

        text, lang = speech_queue.get()
        if text:
            # Set appropriate voice
            if lang == "hi":
                engine.setProperty("voice", hindi_voice)
            else:
                engine.setProperty("voice", english_voice)

            engine.say(text)
            engine.runAndWait()
            speech_queue.task_done()


def chat(query):
    """Handles AI conversation with language context"""
    global chatStr
    
    # Limit chat history
    if len(chatStr) > 5000:
        chatStr = chatStr[-5000:]
    
    # Detect input language
    input_lang = detect(query) if query else 'en'
    
    # Add language context to system message
    system_msg = f"You are a helpful assistant. Respond in {input_lang} if appropriate."
    chatStr += f"User: {query}\nJarvis: "

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[system_msg, chatStr]
        )

        assistant_response = response.text
        formatted_response = f"\n{assistant_response}\n" if "```" in assistant_response else assistant_response
        
        # Detect response language
        try:
            detect_lang = detect(assistant_response)
            detect_lang = 'hi' if detect_lang == 'hi' else 'en'
        except:
            detect_lang = 'en'

        say(formatted_response, detect_lang)
        chatStr += f"{assistant_response}\n"
        return assistant_response

    except Exception as e:
        print(f"Chat error: {e}")
        return "I'm having trouble responding right now."

def takeCommand():
    """Improved voice recognition with proper language priority"""
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return None

    try:
        # First try English
        query = r.recognize_google(audio, language="en-IN")
        print(f"User (English): {query}")
        return query.lower()
    except sr.UnknownValueError:
        try:
            # Fallback to Hindi
            query = r.recognize_google(audio, language="hi-IN")
            print(f"User (Hindi): {query}")
            return query.lower()
        except:
            return None
    except:
        return None

def play_online_music(song_name):
    """Stops current song (if playing) and streams a new song from YouTube."""
    global player

    try:
        # Stop current song if playing
        if player is not None:
            player.stop()
            player = None

        say(f"Searching and streaming {song_name}...")

        # Use yt_dlp to get the best audio URL
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            url = info['url']
        
        # Use VLC to play the new song
        player = vlc.MediaPlayer(url)
        player.play()
            
    
    except Exception as e:
        say("Sorry, I couldn't stream the song.")
        print(f"Error streaming music: {e}")

def take_screenshot():
    """Takes a screenshot and saves it."""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    say("Screenshot taken and saved.")
    
def get_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={wheatherAPI}&q={city}&aqi=no'
    
    # Sending a GET request to fetch the weather data
    response = requests.get(url)
    
    if response.status_code == 200:
        # If the request is successful
        data = response.json()
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        cloud = data['current']['cloud']
        feelslike = data['current']['feelslike_c'] # Temperature perceived by the human body in Celsius
        time = data['current']['last_updated'] 

        say(f"The current temperature in {city} is {temperature} degree celcius and is {description}, humidity is {humidity} percent, the wind speed is {wind_speed} kmph, its {cloud} percent cloudy, it feels like {feelslike} and the current time is {time} hour")
        
    else:
        say("Failed to retrieve data. Please check the city name or API key.")


def shutdown_system():
    """Shuts down the computer."""
    say("Shutting down the system. Goodbye!")
    os.system("shutdown /s /t 0")

def restart_system():
    """Restarts the computer."""
    say("Restarting the system now.")
    os.system("shutdown /r /t 1")

def set_volume(level):
    level = max(0, min(100, level)) 
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_,1,None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(level/100, None)
    say(f"Volume set to {level}%")

def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 1, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    new_volume = min(current_volume + 10, 100)
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
    say(f"Volume increased to {int(new_volume)}%")

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 1, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    new_volume = max(current_volume - 10, 0)
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
    say(f"Volume decreased to {int(new_volume)}%")


def detect_language(text):
    try:
        return detect(text)  # Detects language code (e.g., 'en' for English, 'hi' for Hindi)
    except:
        return "en"  # Default to English if detection fails
    
# def translate_text(text):
#     # Improved translation handling
#     try:
#         translation = asyncio.run(translator.translate(text, dest="hi"))
#         return translation.text  
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text

if __name__ == '__main__':
    print('\nWelcome to Jarvis AI')
    
    # Start speech processing thread
    speech_thread = threading.Thread(target=process_speech_queue, daemon=True)
    speech_thread.start()
    
    # Initial activation message
    say("Jarvis AI is now active.")

    while True:
        query = takeCommand()
        
        if not query:
            continue

        # Improved command handling with regex
        if re.match(r'(open|खोलो)\s+', query, re.IGNORECASE):
            site = re.sub(r'(open|खोलो)\s*', '', query, flags=re.IGNORECASE).strip()
            if "." in site:
                say(f"Opening {site}...")
                webbrowser.open(f"https://{site}")
            else:
                say(f"Searching for {site}...")
                webbrowser.open(f"https://google.com/search?q={site.replace(' ', '+')}")

        elif "play" in query or "चलाओ" in query:
            song_name = query.replace("play", "").replace("चलाओ", "").strip()
            if song_name:
                play_online_music(song_name)
            else:
                say("Please specify a song name.")

        elif "the time" in query or "समय" in query:
            time_now = datetime.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {time_now}")

        elif "open notepad" in query or "नोटपैड खोलो" in query:
            os.startfile("notepad.exe")
            say("Opening Notepad.")
            
        elif "reset chat" in query or "clear history" in query or "चैट रीसेट करो" in query:
            chatStr = ""
            say("Chat history has been reset.")

        elif "take screenshot" in query or "स्क्रीनशॉट लो" in query:
            take_screenshot()

        elif "weather" in query or "मौसम" in query:
            match = re.search(r'\b(?:weather\s*in|मौसम\s*का)\s+([a-zA-Z\sअ-ह]+)', query, re.IGNORECASE)
            if match:
                city = match.group(1).strip()
                get_weather(city)
            else:
                say("Please provide the name of a city.")

        elif "shutdown" in query or "शटडाउन" in query:
            shutdown_system()

        elif "restart" in query or "रिस्टार्ट" in query:
            restart_system()

        elif "set volume to" in query or "वॉल्यूम सेट करो" in query:
            match = re.search(r'set volume to (\d+)', query) or re.search(r'वॉल्यूम सेट करो (\d+)', query)
            if match:
                volume_level = int(match.group(1))
                set_volume(volume_level)

        elif "increase volume" in query or "वॉल्यूम बढ़ाओ" in query:
            increase_volume()

        elif "decrease volume" in query or "वॉल्यूम घटाओ" in query:
            decrease_volume()

        elif "quit" in query or "exit" in query or "बंद करो" in query:
            say("Goodbye sir!")
            sys.exit()

        else:
            # Handle natural language queries
            chat(query)