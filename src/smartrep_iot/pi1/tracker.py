import cv2
import mediapipe as mp
import numpy as np
import time
from datetime import datetime
import threading

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
log_lock = threading.Lock()

# ----------------------------
# CONFIG (IMAGE DIMENSIONS ADDED)
# ----------------------------
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    angle = np.arccos(
        np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    )
    return np.degrees(angle)


def log(msg):
    """Centralized visible logging for demo clarity"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def track_workout():
    log("CAMERA", "Initializing workout tracking system...")

    session_data = {
        "exercise": "bicep_curl",
        "sets": 0,
        "reps_per_set": [],
        "events": [],
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None
    }

    cap = cv2.VideoCapture("/dev/video1")

    # ----------------------------
    # CAMERA INIT LOGS
    # ----------------------------
    if not cap.isOpened():
        log("CAMERA", "ERROR: Camera failed to open")
        exit()

    log("CAMERA", "Camera successfully opened")

    # Set image dimensions (IMPORTANT FOR CONSISTENCY)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    log("CAMERA", f"Frame size set to {FRAME_WIDTH}x{FRAME_HEIGHT}")

    current_reps = 0
    stage = None
    last_rep_time = time.time()

    log("CAMERA", "Starting pose detection loop...")

    while True:
        ret, frame = cap.read()

        if not ret:
            log("CAMERA", "WARNING: Camera read failed, retrying...")
            time.sleep(0.5)
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # ----------------------------
        # POSE DETECTION LOG
        # ----------------------------
        if results.pose_landmarks:
            log("CAMERA", "Pose detected")
            movement_detected = True

            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[12].x, landmarks[12].y]
            elbow = [landmarks[14].x, landmarks[14].y]
            wrist = [landmarks[16].x, landmarks[16].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            log("CAMERA", f"Elbow angle: {angle:.2f}")

            # Rep logic
            if angle < 50:
                stage = "up"
                movement_detected = True
                log("CAMERA", "Stage: UP position detected")

            if angle > 150 and stage == "up":
                stage = "down"
                current_reps += 1
                last_rep_time = time.time()


                movement_detected = True
                log("CAMERA", f"REP COUNTED → Total reps: {current_reps}")

                session_data["events"].append({
                    "type": "rep",
                    "timestamp": datetime.utcnow().isoformat(),
                    "angle": angle
                })

        # ----------------------------
        # SET DETECTION LOG
        # ----------------------------
        if time.time() - last_rep_time > 20 and current_reps > 0:
            session_data["sets"] += 1
            session_data["reps_per_set"].append(current_reps)

            log("CAMERA", f"SET COMPLETED → Set {session_data['sets']} | Reps: {current_reps}")

            session_data["events"].append({
                "type": "set_complete",
                "timestamp": datetime.utcnow().isoformat(),
                "reps": current_reps
            })

            current_reps = 0
            last_rep_time = time.time()

        # ----------------------------
        # EXIT CONDITION LOG
        # ----------------------------
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            log("CAMERA", "Manual stop triggered by user")
            break

    cap.release()
    cv2.destroyAllWindows()

    session_data["end_time"] = datetime.utcnow().isoformat()

    log("CAMERA", "Workout session ended successfully")

    return session_data


def log(source, message):
    with log_lock:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{source}] {message}")