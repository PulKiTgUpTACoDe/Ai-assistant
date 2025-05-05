import cv2
from ultralytics import YOLO
from PIL import Image
import google.genai as genai
import os

try:
    yolo_model = YOLO('yolov8s.pt')
    YOLO_AVAILABLE = True
except Exception as e:
    yolo_model = None
    YOLO_AVAILABLE = False
    print(f"Warning: Could not load YOLOv8 model: {e}")
    print("Object detection functionality will be limited.")

cap = cv2.VideoCapture(0) 

if cap.isOpened():
    CAMERA_AVAILABLE = True

else:
    CAMERA_AVAILABLE = False
    print("Warning: Could not open camera.")
    print("Visual analysis functionality will be disabled.")

try:
    gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    GEMINI_VISION_MODEL_NAME = "gemini-2.5-flash-preview-04-17" 
    GEMINI_AVAILABLE = True

except Exception as e:
    gemini_client = None
    GEMINI_AVAILABLE = False
    print(f"Warning: Gemini API not configured for vision: {e}")
    print("Gemini vision functionality will be disabled.")


def analyze_visual_input(query: str) -> dict:

    if not CAMERA_AVAILABLE:
        return {"result": "Visual analysis is unavailable: Camera not accessible."}

    ret, frame = cap.read()

    if not ret:
        return {"result": "Visual analysis failed: Could not read frame from camera."}

    if GEMINI_AVAILABLE and query:
        try:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            contents = [query, image]
            response = gemini_client.models.generate_content(
                model=GEMINI_VISION_MODEL_NAME,
                contents=contents
            )
            # Release the captured frame resource
            del frame
            return {"result": response.text}

        except Exception as e:
            # If Gemini fails, fall back to YOLO if available
            print(f"Gemini vision analysis failed: {e}. Falling back to YOLO detection if available.")
            if not YOLO_AVAILABLE:
                 del frame
                 return {"result": f"Visual analysis failed after Gemini error: {str(e)} and YOLO is not available."}

    if YOLO_AVAILABLE:
         try:
            results = yolo_model(frame, verbose=False)
            detected_items = []
            for result in results:
                for box in result.boxes:
                     confidence = box.conf[0]
                     class_id = box.cls[0]
                     label = yolo_model.names[int(class_id)]
                     # Optionally filter low confidence detections
                     if confidence > 0.5:
                         detected_items.append(label)

            # Release the captured frame resource
            del frame

            if detected_items:
                unique_detected_items = list(set(detected_items))
                return {"result": "Detected objects: " + ", ".join(unique_detected_items)}
            else:
                return {"result": "No prominent objects detected by YOLO."}

         except Exception as e:
             # Release the captured frame resource
             del frame
             return {"result": f"YOLO detection failed: {str(e)}"}

    else:
        # Release the captured frame resource
        del frame
        return {"result": "Visual analysis is unavailable: Neither Gemini Vision nor YOLO is configured or available."}
