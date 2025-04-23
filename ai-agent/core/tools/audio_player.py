# audio_player.py
import yt_dlp
import vlc
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

# Global player control
music_player = None
playback_thread = None
stop_event = threading.Event()

class MusicPlayer:
    def __init__(self):
        self.instance = vlc.Instance('--no-xlib --quiet')
        self.player = self.instance.media_player_new()
        self.stop_requested = threading.Event()

    def play(self, url):
        """Plays music and monitors stop requests"""
        self.player.set_media(self.instance.media_new(url))
        self.player.play()
        
        # Keep checking playback status until stopped or finished
        while not self.stop_requested.is_set() and self.player.is_playing():
            time.sleep(0.1)
        
        if self.stop_requested.is_set():
            self.player.stop()

    def stop(self):
        """Signals the playback to stop"""
        self.stop_requested.set()

def play_music(song_name: str) -> dict:
    global music_player, playback_thread, stop_event
    
    # Stop any existing playback first
    stop_music()

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'noplaylist': True,
            'quiet': True,
            'socket_timeout': 10
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_name, download=False)
            if not info.get('entries'):
                return {"error": "Song not found"}
            
            url = info['entries'][0]['url']
            
            # Create new player and thread
            music_player = MusicPlayer()
            playback_thread = threading.Thread(target=music_player.play, args=(url,))
            stop_event.clear()
            playback_thread.start()
            
            return {"result": f"Now playing: {info['entries'][0]['title']}"}

    except Exception as e:
        return {"error": str(e)}

def stop_music():
    """Stops currently playing music and cleans up resources"""
    global music_player, playback_thread, stop_event
    
    if music_player is not None:
        # Signal stop request
        music_player.stop()
        
        # Wait for thread to finish
        if playback_thread.is_alive():
            playback_thread.join(timeout=2)
        
        # Cleanup
        music_player = None
        playback_thread = None
        stop_event.set()
    
    return {"result": "Music stopped"}