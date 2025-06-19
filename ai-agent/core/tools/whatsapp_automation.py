import pywhatkit as kit
import pyautogui as pg
import time
import os
from datetime import datetime, timedelta
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Literal
import subprocess
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

now = datetime.now() + timedelta(minutes=1)

llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    model="gemini-2.0-flash",
    temperature=0.7
)

@tool
def is_whatsapp_desktop_installed() -> dict:
    """Check if the whatsapp app is installed on desktop or not"""

    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-AppxPackage -Name "*WhatsApp*"'],
            capture_output=True, text=True
        )
        return {"result": "WhatsApp" in result.stdout}
    except Exception as e:
        return {"result": False}

@tool
def whatsapp_automation_app(recipient: str, message: str) -> dict:
    """Sends message on whatsApp app which is downloaded on desktop
    Args:
        recipient: The Name or phone number (for individuals) or Group Name(for groups).
        message: The message to send. Optional if sending only an image.
    """
    try:
        pg.press('win')
        time.sleep(1)
        pg.write('whatsap')
        time.sleep(1)
        pg.press('enter')
        time.sleep(5)

        pg.press('esc',2,0.2)
        pg.hotkey('ctrl','a')
        pg.press('backspace')

        pg.write(recipient)
        time.sleep(2)
        pg.press('down')
        pg.press('enter')
        time.sleep(1)
        pg.write(message)
        time.sleep(1)
        pg.press('enter')
        return {"result": f"Message sent to {recipient} via app"}
    
    except Exception as e:
        return {"result": f"Failed to send WhatsApp message via app: {str(e)}"}

@tool
def whatsapp_automation_web(
    phone_number: str,
    message: Optional[str] = None,
    image_path: Optional[str] = None,
    caption: Optional[str] = "",
    time_hour: Optional[int] = None,
    time_minute: Optional[int] = None,
    recipient_type: Literal["individual", "group"] = "individual"
) -> dict:
    """
    Sends a WhatsApp message, image, or both to an individual or group on webApp.
    
    Args:
        recipient_number: The phone number (for individuals) or group ID/invite link (for groups).
        message: The message to send. Optional if sending only an image.
        image_path: The path to the image file. Optional if sending only a message.
        caption: Optional caption for the image.
        time_hour: Only set the hour when user has asked to do it else set it to 0 hours. The hour (24-hour format) to send the message/image. If None, sends immediately.
        time_minute: Set the minute when user says to set else set it to 0 minutes. The minute to send the message/image. If None, sends immediately.
        recipient_type: Whether the recipient is an "individual" or a "group".

    Returns:
        A dictionary with the result or error message.
    """
        
    try:
        if recipient_type == "individual":
            if message and image_path:
                if time_hour is None or time_minute is None:
                    kit.sendwhatmsg(phone_number, message, now.hour, now.minute)
                    time.sleep(10)
                    kit.sendwhats_image(phone_number, image_path, caption)
                    return {"result": f"Message and image sent to {phone_number} via web"}
                else:
                    kit.sendwhatmsg(phone_number, message, time_hour, time_minute)
                    kit.sendwhats_image(phone_number, image_path, caption, time_hour, time_minute)
                    return {"result": f"Message and image scheduled for {phone_number} at {time_hour}:{time_minute}"}

            elif message:
                if time_hour is None or time_minute is None:
                    kit.sendwhatmsg(phone_number, message, now.hour, now.minute)
                    return {"result": f"Message sent to {phone_number} via web"}
                else:
                    kit.sendwhatmsg(phone_number, message, time_hour, time_minute)
                    return {"result": f"Message scheduled for {phone_number} at {time_hour}:{time_minute}"}

            elif image_path:
                if time_hour is None or time_minute is None:
                    kit.sendwhats_image(phone_number, image_path, caption)
                    return {"result": f"Image sent to {phone_number} via web"}
                else:
                    kit.sendwhats_image(phone_number, image_path, caption, time_hour, time_minute)
                    return {"result": f"Image scheduled for {phone_number} at {time_hour}:{time_minute}"}
            else:
                return {"result": "Please provide a message or image."}

        elif recipient_type == "group":
            if message and image_path:
                kit.sendwhatmsg_to_group(phone_number, message, now.hour, now.minute)
                time.sleep(10)
                kit.sendwhats_image_to_group(phone_number, image_path, caption)
                return {"result": f"Message and image sent to group {phone_number}"}
            elif message:
                kit.sendwhatmsg_to_group(phone_number, message, now.hour, now.minute)
                return {"result": f"Message sent to group {phone_number}"}
            elif image_path:
                kit.sendwhats_image_to_group(phone_number, image_path, caption)
                return {"result": f"Image sent to group {phone_number}"}
            else:
                return {"result": "Please provide a message or image."}
    except Exception as e:
        return {"result": f"Failed to send WhatsApp message/image: {str(e)}"}


tools = [is_whatsapp_desktop_installed, whatsapp_automation_app, whatsapp_automation_web]
whatsapp_langgraph_agent = create_react_agent(llm, tools)

def get_message_for_whatsapp(query: str) -> dict:
    messages = [("user", query)]
    result = whatsapp_langgraph_agent.invoke({"messages": messages})
    return {"result": result["messages"][-1].content}

    
