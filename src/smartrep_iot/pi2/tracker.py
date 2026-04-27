import cv2
import mediapipe as mp
import numpy as np
import time
from datetime import datetime

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    angle = np.arccos(
        np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    )
    return np.degrees(angle)


def track_workout():
    session_data = {
        "exercise": "bicep_curl",
        "sets": 0,
        "reps_per_set": [],
        "events": [],
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None
    }

    cap = cv2.VideoCapture(0)

    current_reps = 0
    stage = None
    last_rep_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[12].x, landmarks[12].y]
            elbow = [landmarks[14].x, landmarks[14].y]
            wrist = [landmarks[16].x, landmarks[16].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            # Rep logic
            if angle < 50:
                stage = "up"

            if angle > 150 and stage == "up":
                stage = "down"
                current_reps += 1
                last_rep_time = time.time()

                session_data["events"].append({
                    "type": "rep",
                    "timestamp": datetime.utcnow().isoformat(),
                    "angle": angle
                })

        # Set detection
        if time.time() - last_rep_time > 20 and current_reps > 0:
            session_data["sets"] += 1
            session_data["reps_per_set"].append(current_reps)

            session_data["events"].append({
                "type": "set_complete",
                "timestamp": datetime.utcnow().isoformat(),
                "reps": current_reps
            })

            current_reps = 0
            last_rep_time = time.time()

        # Exit condition
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    session_data["end_time"] = datetime.utcnow().isoformat()

    return session_data