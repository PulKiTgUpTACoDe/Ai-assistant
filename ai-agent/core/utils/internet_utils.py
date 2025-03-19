import webbrowser
import pyautogui
import time

def search_google(query):
    """Opens a Google search for the given query."""
    webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")

def find_and_open_app(app_name):
    """Opens an application using the Windows search bar."""
    try:
        pyautogui.press('win')
        time.sleep(0.1)
        pyautogui.write(app_name)
        time.sleep(0.1)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Error opening app via Windows search: {e}")
        return False 