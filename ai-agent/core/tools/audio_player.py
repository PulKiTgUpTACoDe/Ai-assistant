import yt_dlp
import vlc
import os
import sys

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

player = None

def play_online_music(song_name):
    """Stops current song (if playing) and streams a new song from YouTube."""
    global player

    try:
        if player is not None:
            player.stop()
            player = None

        say(f"Searching and streaming {song_name}...")

        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            url = info['url']

        player = vlc.MediaPlayer(url)
        player.play()

    except Exception as e:
        print(f"Error streaming music: {e}")

def stop_music():
    """Stops the currently playing music."""
    global player
    if player is not None:
        player.stop()
        player = None
        say("Music stopped.") 