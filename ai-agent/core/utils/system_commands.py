import os
import subprocess
import datetime
import sys

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.tools.speech_synthesis import say

def get_time():
    return datetime.datetime.now().strftime("%H:%M")

def shutdown_system():
    """Closes all running applications and shuts down the computer."""
    say("Closing all running applications.")
    close_all_applications()  # Call the function to close apps
    # say("Shutting down the system. Goodbye!")
    os.system("shutdown /s /t 0")

def restart_system():
    """Closes all running applications and restarts the computer."""
    say("Closing all running applications.")
    close_all_applications()  # Call the function to close apps
    # say("Restarting the system now.")
    os.system("shutdown /r /t 1")

def close_all_applications():
    """Closes all running applications using taskkill."""
    try:
        # Get a list of all running processes
        process_list = subprocess.check_output(['tasklist']).decode('utf-8').splitlines()

        # Iterate through the processes and kill them
        for process in process_list:
            process_name = process.split()[0].lower() # Get the process name
            #Exclude system processes. Be very careful with this list.
            if process_name not in ["system", "services.exe", "svchost.exe", "lsass.exe", "wininit.exe", "winlogon.exe","csrss.exe","smss.exe","explorer.exe"]:
                try:
                    subprocess.run(['taskkill', '/f', '/im', process_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except subprocess.CalledProcessError:
                    pass # Handle any errors during task killing
    except Exception as e:
        print(f"Error closing applications: {e}") 