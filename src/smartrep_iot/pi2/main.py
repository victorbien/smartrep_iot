from tracker import track_workout
from ai_coach import generate_coaching
from mqtt_client import publish

def main():

    # -------- PHASE 1: TRACK (NO GPT) --------
    session_data = track_workout()

    # -------- PHASE 2: AI (POST-WORKOUT ONLY) --------
    coaching = generate_coaching(session_data)

    # -------- PHASE 3: PUBLISH --------
    payload = {
        "event": "session_complete",
        "exercise": session_data["exercise"],
        "sets": session_data["sets"],
        "reps_per_set": session_data["reps_per_set"],
        "start_time": session_data["start_time"],
        "end_time": session_data["end_time"],
        "coaching_summary": coaching
    }

    publish(payload)

    print("Session complete + coaching sent to ThingsBoard")
    print(coaching)


if __name__ == "__main__":
    main()