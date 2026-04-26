import cv2
import base64
import time
from openai import OpenAI
from config import OPENAI_API_KEY
import os


# --- Configuration ---
# Set your API Key
client = OpenAI(api_key=OPENAI_API_KEY)
# Resolution reduction for speed
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
# Seconds between frames sent to GPT
ANALYSIS_INTERVAL = 2

def encode_image(image):
    """Encodes a BGR image to base64 string."""
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode('utf-8')

def analyze_frame(base64_image):
    """Sends frame to GPT-4o for evaluation."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "You are a gym coach. Give concise, encouraging feedback in 3-4 sentences, about the posture. Evaluate whether the posture is correct."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def main():
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    print("Starting streaming analysis...")
    
    last_analysis = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        
        # Only analyze every few seconds
        if current_time - last_analysis > ANALYSIS_INTERVAL:
            base64_image = encode_image(frame)
            analysis = analyze_frame(base64_image)
            print(f"GPT Analysis: {analysis}")
            last_analysis = current_time

        # Display (optional, comment out to save CPU)
        cv2.imshow("Live Feed", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
