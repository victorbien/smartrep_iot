from openai import OpenAI
from config import OPENAI_API_KEY
import threading

client = OpenAI(api_key=OPENAI_API_KEY)
log_lock = threading.Lock()

def generate_coaching(session_data):

    prompt = f"""
    Exercise: {session_data['exercise']}
    Sets: {session_data['sets']}
    Reps: {session_data['reps_per_set']}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a gym coach. Give concise, encouraging feedback in 3-4 sentences."},
            {"role": "user", "content": prompt}
        ]
    )

    log("AI COACHING", response.choices[0].message.content)
    return response.choices[0].message.content


def log(source, message):
    with log_lock:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{source}] {message}")