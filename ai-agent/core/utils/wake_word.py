import pvporcupine
import pyaudio
import numpy as np
from threading import Event

class WakeWordDetector:
    def __init__(self, access_key, wake_word="bumblebee"):
        self.access_key = access_key
        self.wake_word = wake_word
        self.detected_event = Event()
        self.porcupine = None
        self.audio_stream = None
        
    def initialize(self):
        """Initialize the wake word detector"""
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=[self.wake_word]
            )
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
                stream_callback=self.audio_callback
            )
        except Exception as e:
            raise RuntimeError(f"Wake word init failed: {str(e)}")

    def audio_callback(self, in_data, *_):
        if self.porcupine is not None:
            pcm = np.frombuffer(in_data, dtype=np.int16)
            result = self.porcupine.process(pcm)
            if result >= 0:
                self.detected_event.set()
        return (in_data, pyaudio.paContinue)

    def start_listening(self):
        """Start listening for wake word"""
        self.detected_event.clear()
        self.audio_stream.start_stream()

    def stop(self):
        """Clean up resources"""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.porcupine:
            self.porcupine.delete()
        if self.audio:
            self.audio.terminate()