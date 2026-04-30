import time
from datetime import datetime
import RPi.GPIO as GPIO
import threading

from config import EQUIPMENT, CHAIR, AVAILABLE, OCCUPIED, THRESHOLD, CHANNEL, SLEEP_TIME
from adc import read_adc
from led import setup_leds, update_led
from session_manager import SessionManager
from mqtt_client import publish
from tracker import track_workout
from ai_coach import generate_coaching

log_lock = threading.Lock()

# Setup
setup_leds(EQUIPMENT)
session_mgr = SessionManager(EQUIPMENT)

# shared state
session_data = {}
workout_done = False


# ------------------------
# THREAD 1: CAMERA TRACKER
# ------------------------
def workout_thread():
    global session_data, workout_done

    session_data = track_workout()

    coaching = generate_coaching(session_data)

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

    workout_done = True


# ------------------------
# THREAD 2: LED + FSR LOOP
# ------------------------
def sensor_led_thread():
    try:
        while True:
            overall_state = {}

            for name, eq in EQUIPMENT.items():

                value = read_adc(eq[CHANNEL])

                if name == CHAIR:
                    available = value < eq[THRESHOLD]
                else:
                    available = value > eq[THRESHOLD]

                update_led(eq, available)
                session_mgr.handle(name, available)

                overall_state[name] = AVAILABLE if available else OCCUPIED

                log("GYM EQUIPMENT", f"{name}: {overall_state[name]}")

            publish(overall_state)
            print("-" * 30)
            time.sleep(SLEEP_TIME)

    finally:
        GPIO.cleanup()


# ------------------------
# MAIN
# ------------------------
def main():

    t1 = threading.Thread(target=workout_thread)
    t2 = threading.Thread(target=sensor_led_thread)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def log(source, message):
    with log_lock:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{source}] {message}")

if __name__ == "__main__":
    main()
    
