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
from mistralai.client import MistralClient
from config import apikey, wheatherAPI

# Initialize Mistral AI client
MISTRAL_API_KEY = apikey
client = MistralClient(api_key=apikey)

# Text-to-Speech setup moved to the processing thread
speech_queue = queue.Queue()
control_queue = queue.Queue()

# Global variables
chatStr = ""
speaking = False  # Track if AI is speaking
player = None

def stop_speaking():
    control_queue.put("stop")

def say(text):
    """Speaks the given text while allowing interruptions"""
    global speaking
    speaking = True

    # Print response in the terminal
    if "```" in text:
        print("\n" + text + "\n")  # Display formatted code
    else:
        print(f"\nJarvis: {text}")

    # Add text to the speech queue
    speech_queue.put(text)

def process_speech_queue():
    """Processes speech requests in a dedicated thread"""
    engine = pyttsx3.init()
    while True:
        try:
            cmd = control_queue.get_nowait()
            if cmd == "stop":
                engine.stop()
        except queue.Empty:
            pass
        
        text = speech_queue.get()
        if text:
            engine.say(text)
            engine.runAndWait()
            speech_queue.task_done()

def chat(query):
    """Handles AI conversation and formatted code output"""
    global chatStr

    chatStr += f"User: {query}\nJarvis: "

    try:
        response = client.chat(
            model="mistral-tiny",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chatStr}
            ]
        )

        assistant_response = response.choices[0].message.content
        formatted_response = f"\n{assistant_response}\n" if "```" in assistant_response else assistant_response
        
        say(formatted_response)
        chatStr += f"{assistant_response}\n"
        return assistant_response

    except Exception as e:
        print(f"Error in chat function: {e}")
        return "Sorry, I encountered an error."

def takeCommand():
    """Listens for voice input and allows interruptions"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User: {query}")

            if speaking:
                stop_speaking()
            return query.lower()
        
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return None
        except Exception as e:
            print(f"Error in takeCommand: {e}")
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
    os.system("shutdown /s /t 1")

def restart_system():
    """Restarts the computer."""
    say("Restarting the system now.")
    os.system("shutdown /r /t 1")

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

        if "open" in query:
            site = query.replace("open ", "").strip()
            if "." in site:
                say(f"Opening {site}...")
                webbrowser.open(f"https://{site}")
            else:
                say(f"Searching for {site}...")
                webbrowser.open(f"https://google.com/search?q={site.replace(' ', '+')}")
        elif "play" in query:
            song_name = query.replace("play", "").strip()
            if song_name:
                play_online_music(song_name)
            else:
                say("Please specify a song name.")
        elif "the time" in query:
            time_now = datetime.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {time_now}")
        elif "open notepad" in query:
            os.startfile("notepad.exe")
        elif "reset chat" in query or "clear history" in query:
            chatStr = ""
            say("Chat history has been reset.")
        elif "take screenshot" in query:
            take_screenshot()
        elif "weather" in query:
            match = re.search(r'\b(?:weather\s*in|in\s*the\s*city\s*of)\s+([a-zA-Z\s]+)', query, re.IGNORECASE)
            if match:
                city = match.group(1).strip()
                get_weather(city)
            else:
                say("Please give an appropriate name of the city")
        elif "shutdown" in query:
            shutdown_system()
        elif "restart" in query:
            restart_system()
        elif "quit" in query or "exit" in query:
            say("Goodbye sir!")
            sys.exit()
        else:
            chat(query)
