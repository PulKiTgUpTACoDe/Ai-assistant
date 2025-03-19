import pyttsx3
import queue

speech_queue = queue.Queue()
control_queue = queue.Queue()

def say(text, lang="en"):

    # Preserve code blocks in English
    if "```" in text:
        print(f"\n{text}\n")
        speech_queue.put((text, "en"))
        return

    print(f"\nAI: {text}")
    speech_queue.put((text, lang))

def process_speech_queue():
    # Processes speech requests in a dedicated thread
    engine = pyttsx3.init()
    
    # Get available voices and identify Hindi voice
    voices = engine.getProperty('voices')
    
    # Set Hindi and English voices
    hindi_voice = voices[2].id 
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

            engine.say(text+" ")
            engine.runAndWait()
            speech_queue.task_done() 