import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
import sys
import threading
import queue
from mistralai.client import MistralClient
from config import apikey

# Initialize Mistral AI client
MISTRAL_API_KEY = apikey
client = MistralClient(api_key=MISTRAL_API_KEY)

# Text-to-Speech setup moved to the processing thread
speech_queue = queue.Queue()
control_queue = queue.Queue()

# Global variables
chatStr = ""
speaking = False  # Track if AI is speaking

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
        # Check for stop commands
        try:
            cmd = control_queue.get_nowait()
            if cmd == "stop":
                engine.stop()
        except queue.Empty:
            pass
        
        # Process speech requests
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
        elif "play music" in query:
            musicPath = "C:\\Users\\mande\\.vscode\\Programs\\Projects\\Spotify Project\\Songs\\Safari\\Suzume no Tojimari Theme Song.mp3"
            os.startfile(musicPath)
        elif "the time" in query:
            time_now = datetime.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {time_now}")
        elif "open notepad" in query:
            os.startfile("notepad.exe")
        elif "reset chat" in query:
            chatStr = ""
            say("Chat history has been reset.")
        elif "quit" in query or "exit" in query:
            say("Goodbye sir!")
            sys.exit()
        else:
            chat(query)