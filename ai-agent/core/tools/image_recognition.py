from .object_detection import gemini_client
import pyautogui

try:
    geminiClient = gemini_client
    GEMINI_VISION_MODEL_NAME = "gemini-2.5-flash-preview-04-17" 
    GEMINI_AVAILABLE = True

except Exception as e:
    geminiClient = None
    GEMINI_AVAILABLE = False
    print(f"Warning: Gemini API not configured for vision: {e}")
    print("Gemini image processing functionality will be disabled.")

def analyze_image(query: str) -> dict:
    frame = pyautogui.screenshot()

    if GEMINI_AVAILABLE and query:
        try:
            image = frame
            contents = [query, image]
            response = geminiClient.models.generate_content(
                model=GEMINI_VISION_MODEL_NAME,
                contents=contents
            )
            # Release the captured frame resource
            del frame
            return {"result": response.text}

        except Exception as e:
            print(f"Error in image capturing or processing: {e}.")

    else:
        del frame
        return {"result": "Image analysis is unavailable"}