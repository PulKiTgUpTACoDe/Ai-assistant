import yt_dlp
import vlc
import os
import sys
import threading
import time

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

# Global player control
music_player = None
playback_thread = None

def play_music(song_name: str) -> dict:
    global music_player, playback_thread
    
    class MusicPlayer:
        def __init__(self):
            self.instance = vlc.Instance('--no-xlib --quiet')
            self.player = self.instance.media_player_new()
            self.running = False

        def play(self, url):
            self.player.set_media(self.instance.media_new(url))
            self.player.play()
            self.running = True
            while self.running and self.player.get_state() != vlc.State.Ended:
                time.sleep(0.5)

        def stop(self):
            self.running = False
            self.player.stop()

    def _play_music(song):
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'noplaylist': True,
            'quiet': True,
            'socket_timeout': 10
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song, download=False)
                if not info.get('entries'):
                    return {"error": "Song not found"}
                
                url = info['entries'][0]['url']
                player = MusicPlayer()
                player.play(url)
                return {"result": f"Played: {info['entries'][0]['title']}"}

        except Exception as e:
            return {"error": str(e)}

    # Stop any existing playback
    if music_player:
        music_player.stop()
        playback_thread.join()

    # Start new playback thread
    music_player = MusicPlayer()
    playback_thread = threading.Thread(target=_play_music, args=(song_name,))
    playback_thread.start()
    
    return {"result": f"Now playing: {song_name}"}