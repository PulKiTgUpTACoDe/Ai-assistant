import pyautogui
import os
import sys

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

def take_screenshot():
    """Takes a screenshot and saves it."""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    # say("Screenshot taken and saved.") 