import pyttsx3
import queue

speech_queue = queue.Queue()
control_queue = queue.Queue()

def say(text, lang="en"):
    if "```" in text:
        print(f"\n{text}\n")
        speech_queue.put((text, "en"))
        return

    print(f"\nAI: {text}")
    speech_queue.put((text, lang))
    control_queue.put("speak")  # Signal to start speaking

def process_speech_queue():
    # Processes speech requests in a dedicated thread
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    
    # Set Hindi and English voices
    hindi_voice = voices[2].id 
    english_voice = voices[0].id

    while True:
        try:
            cmd = control_queue.get_nowait()
            if cmd == "stop":
                engine.stop()
            elif cmd == "speak":
                text, lang = speech_queue.get()
                if text:
                    if lang == "hi":
                        engine.setProperty("voice", hindi_voice)
                    else:
                        engine.setProperty("voice", english_voice)

                    engine.say(text+" ")
                    engine.runAndWait()
                    speech_queue.task_done() 
        except queue.Empty:
            pass 