import time
import RPi.GPIO as GPIO

from config import EQUIPMENT, CHAIR, AVAILABLE, OCCUPIED, THRESHOLD, CHANNEL, SLEEP_TIME
from adc import read_adc
from led import setup_leds, update_led
from session_manager import SessionManager
from mqtt_client import publish

# Setup
setup_leds(EQUIPMENT)
session_mgr = SessionManager(EQUIPMENT)

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

            print(f"{name}: {overall_state[name]}")

        # Optional: publish all states together
        publish(overall_state)
        print("-" * 30)
        time.sleep(SLEEP_TIME)

finally:
    GPIO.cleanup()

