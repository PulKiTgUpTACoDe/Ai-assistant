import speech_recognition as sr

def takeCommand():
    """Improved voice recognition with proper language priority"""
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = r.listen(source, timeout=20, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None

    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"\nUser: {query}")
        return query.lower()
    # except sr.UnknownValueError:
    #     try:
    #         # Fallback to Hindi
    #         query = r.recognize_google(audio, language="hi-IN")
    #         print(f"User (Hindi): {query}")
    #         return query.lower()
    #     except:
    #         return None
    except:
        return None