import speech_recognition as sr
from . import speech_synthesis
import threading

def takeCommand():
    """Improved voice recognition with proper language priority"""
    r = sr.Recognizer()
    r.energy_threshold = 3000 
    r.pause_threshold = 1.5  
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return None

    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"\nUser: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def get_confirmation(prompt):
    speech_synthesis.say(prompt + " Please say yes or no.")
    response = takeCommand()
    return response and response.lower() in ['yes', 'y', 'yeah', 'confirm']  