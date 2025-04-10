from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import sys

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

def set_volume(level):
    level = max(0, min(100, level)) 
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_,1,None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(level/100, None)
    # say(f"Volume set to {level}%")

def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, 1, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    new_volume = min(current_volume + 10, 100)
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
    # say(f"Volume increased to {int(new_volume)}%")

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 1, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    new_volume = max(current_volume - 10, 0)
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
    # say(f"Volume decreased to {int(new_volume)}%") 