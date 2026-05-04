import cv2
import time
import uuid
import numpy as np
import mediapipe as mp

from fsr import read_fsr
from mqtt_client import publish
from ai_coach import generate_coaching

# -------------------------------
# MEDIAPIPE INIT
# -------------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# -------------------------------
# HELPER: ANGLE
# -------------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine_angle))
    return angle

# -------------------------------
# DETECTORS
# -------------------------------
def detect_bicep_curl(landmarks):
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    angle = calculate_angle(shoulder, elbow, wrist)

    return angle

def detect_squat(landmarks):
    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    angle = calculate_angle(hip, knee, ankle)

    return angle

def track_workout():
    # -------------------------------
    # CONFIG
    # -------------------------------
    MAX_SETS = 3
    REPS_PER_SET = 12
    SESSION_TIMEOUT = 10

    angles_per_rep = []
    current_rep_angles = []

    EXERCISE_TYPE = "bicep_curl"  # or "squat"

    # -------------------------------
    # STATE
    # -------------------------------
    session_active = False
    session_id = None

    set_count = 0
    rep_count = 0
    bad_reps = 0

    last_activity_time = 0
    prev_pressure = 0
    lift_detected = False

    stage = None  # "up" / "down"

    # -------------------------------
    # CAMERA INIT
    # -------------------------------
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        raise RuntimeError("Camera failed to open")

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        pressure = read_fsr()
        current_time = time.time()

        # ---------------------------
        # SESSION START
        # ---------------------------
        if pressure and not session_active:
            session_active = True
            session_id = str(uuid.uuid4())

            set_count = 0
            rep_count = 0
            bad_reps = 0
            stage = None

            print(f"Session started: {session_id}")

        # ---------------------------
        # ACTIVITY TRACKING
        # ---------------------------
        if pressure:
            last_activity_time = current_time

        # ---------------------------
        # FSR LIFT-RETURN END
        # ---------------------------
        if prev_pressure == 1 and pressure == 0:
            lift_detected = True

        if lift_detected and pressure == 1:
            print("Lift-return detected → session end")
            session_active = False

        prev_pressure = pressure

        # ---------------------------
        # CAMERA FRAME
        # ---------------------------
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed")
            continue

        # ---------------------------
        # TRACKING
        # ---------------------------
        if session_active:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                if EXERCISE_TYPE == "bicep_curl":
                    angle = detect_bicep_curl(landmarks)
                    
                    current_rep_angles.append(angle)

                    # Rep logic
                    if angle > 160:
                        stage = "down"
                    if angle < 45 and stage == "down":
                        stage = "up"
                        rep_count += 1
                        print(f"Rep: {rep_count}")
                        
                        # Save angles for this rep
                        if current_rep_angles:
                            rep_summary = {
                                "rep": rep_count,
                                "min": min(current_rep_angles),
                                "max": max(current_rep_angles)
                            }
                            
                            angles_per_rep.append(rep_summary)

                    # Bad form
                    if angle > 170:
                        bad_reps += 1

                elif EXERCISE_TYPE == "squat":
                    angle = detect_squat(landmarks)
                    
                    current_rep_angles.append(angle)

                    if angle > 160:
                        stage = "up"
                    if angle < 70 and stage == "up":
                        stage = "down"
                        rep_count += 1
                        print(f"Rep: {rep_count}")
                        
                        # Save angles for this rep
                        if current_rep_angles:
                            rep_summary = {
                                "rep": rep_count,
                                "min": min(current_rep_angles),
                                "max": max(current_rep_angles)
                            }
                            
                            angles_per_rep.append(rep_summary)

                    if angle > 175:
                        bad_reps += 1

                # -------------------
                # SET CONTROL
                # -------------------
                if rep_count >= REPS_PER_SET:
                    set_count += 1
                    rep_count = 0
                    print(f"Set {set_count} completed")

                if set_count >= MAX_SETS:
                    print("Workout completed")
                    session_active = False

        # ---------------------------
        # DISPLAY
        # ---------------------------
        cv2.imshow("Tracking", frame)

        # ---------------------------
        # MANUAL END
        # ---------------------------
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Manual stop")
            session_active = False

        # ---------------------------
        # TIMEOUT END
        # ---------------------------
        if session_active and (current_time - last_activity_time > SESSION_TIMEOUT):
            print("Session timeout")
            session_active = False

        # ---------------------------
        # AI COACHING
        # ---------------------------
        if not session_active and session_id is not None:
            print("Triggering AI Coaching...")

            session_data = {
                "exercise": EXERCISE_TYPE,
                "sets": set_count,
                "reps_per_set": rep_count,
                "bad_reps": bad_reps,
                "form_score": max(0, 100 - bad_reps * 10),
                "angle_data": angles_per_rep
            }

            feedback = generate_coaching(session_data)

            publish({
                "session_id": session_id,
                "exercise": EXERCISE_TYPE,
                "sets": set_count,
                "reps_per_set": rep_count,
                "bad_reps": bad_reps,
                "feedback": feedback
            })

            print("AI Coaching Complete")

            # RESET
            session_id = None
            lift_detected = False
            time.sleep(2)

    # -------------------------------
    # CLEANUP
    # -------------------------------
    cap.release()
    cv2.destroyAllWindows()

