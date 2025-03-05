import pyautogui
from ..audio.text_to_speech import say

def take_screenshot():
    """Takes a screenshot and saves it."""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    say("Screenshot taken and saved.")