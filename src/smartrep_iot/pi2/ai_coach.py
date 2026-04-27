from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

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

    return response.choices[0].message.content