import speech_recognition as sr
import speech_synthesis
def takeCommand():
    """Improved voice recognition with proper language priority"""
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.pause_threshold = 1
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = r.listen(source)
        except sr.WaitTimeoutError:
            return None

    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"\nUser: {query}")
        return query.lower()
    except:
        return None 
    
def get_confirmation(prompt):
    speech_synthesis.say(prompt + " Please say yes or no.")
    response = takeCommand().lower()
    return response in ['yes', 'y', 'yeah', 'confirm']