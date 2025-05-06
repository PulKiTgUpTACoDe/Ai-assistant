import pywhatkit as kit
import pyautogui
from datetime import datetime,time, timedelta
from langchain.tools import tool
from typing import Any, Optional, Literal
import pytz

now = datetime.now(pytz.timezone("Asia/Kolkata")) + timedelta(minutes=1)

def send_image_to_group(group_id: str, image_path: str, caption: str = "") -> dict:
    """
    Simulates sending an image to a WhatsApp group using pyautogui.
    
    Args:
        group_id: The group ID or invite link of the WhatsApp group.
        image_path: The path to the image file.
        caption: Optional caption for the image.
    
    Returns:
        A dictionary with the result or error message.
    """
    try:
        # Open the group chat
        kit.sendwhatmsg_to_group(group_id, "", now.hour, now.minute)  # Open the group chat
        time.sleep(5)  # Wait for the chat to load

        # Attach the image
        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(2)
        pyautogui.write(image_path)
        pyautogui.press('enter') 
        time.sleep(2)

        # Add the caption (if any)
        if caption:
            pyautogui.write(caption)
            time.sleep(1)

        pyautogui.press('enter')
        time.sleep(2)

        return {"result": f"Image sent to group {group_id} immediately"}
    except Exception as e:
        return {"error": f"Failed to send image to group: {str(e)}"}
    
@tool
def whatsapp_automation(
    recipient: str,
    message: Optional[str] = None,
    image_path: Optional[str] = None,
    caption: Optional[str] = "",
    time_hour: Optional[int] = None,
    time_minute: Optional[int] = None,
    recipient_type: Literal["individual", "group"] = "individual"
) -> dict:
    """
    Sends a WhatsApp message, image, or both to an individual or group.
    
    Args:
        recipient: The phone number (for individuals) or group ID/invite link (for groups).
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
                    kit.sendwhatmsg(recipient, message, now.hour, now.minute) 
                    kit.sendwhats_image(recipient, image_path, caption)  
                    return {"result": f"Message and image sent to {recipient} immediately"}
                else:
                    kit.sendwhatmsg(recipient, message, time_hour, time_minute) 
                    kit.sendwhats_image(recipient, image_path, caption, time_hour, time_minute)
                    return {"result": f"Message and image scheduled to be sent to {recipient} at {time_hour}:{time_minute}"}
                
            elif message:
                if time_hour is None or time_minute is None:
                    kit.sendwhatmsg(recipient, message, now.hour, now.minute) 
                    return {"result": f"Message sent to {recipient} immediately"}
                else:
                    kit.sendwhatmsg(recipient, message, time_hour, time_minute) 
                    return {"result": f"Message scheduled to be sent to {recipient} at {time_hour}:{time_minute}"}
                
            elif image_path:
                if time_hour is None or time_minute is None:
                    kit.sendwhats_image(recipient, image_path, caption) 
                    return {"result": f"Image sent to {recipient} immediately"}
                else:
                    kit.sendwhats_image(recipient, image_path, caption, time_hour, time_minute) 
                    return {"result": f"Image scheduled to be sent to {recipient} at {time_hour}:{time_minute}"}
            else:
                return {"result": "Either a message or an image must be provided."}
        
        elif recipient_type == "group":
            if message and image_path:
                kit.sendwhatmsg_to_group(recipient, message, now.hour, now.minute)  
                kit.sendwhats_image_to_group(recipient, image_path, caption)
                return {"result": f"Message and image sent to group {recipient} immediately"}
            
            elif message:
                kit.sendwhatmsg_to_group(recipient, message, now.hour, now.minute)  
                return {"result": f"Message sent to group {recipient} immediately"}
            
            elif image_path:
                kit.sendwhats_image_to_group(recipient, image_path, caption) 
                return {"result": f"Image sent to group {recipient} immediately"}
            else:
                return {"result": "Either a message or an image must be provided."}
        
        else:
            return {"result": "Invalid recipient type. Must be 'individual' or 'group'."}
    
    except Exception as e:
        return {"result": f"Failed to send WhatsApp message/image: {str(e)}"}