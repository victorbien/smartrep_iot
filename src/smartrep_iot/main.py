import time
import RPi.GPIO as GPIO

from config import EQUIPMENT
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
            value = read_adc(eq["channel"])
            occupied = value > eq["threshold"]

            update_led(eq, occupied)
            session_mgr.handle(name, occupied)

            overall_state[name] = "occupied" if occupied else "available"

            print(f"{name}: {value}")

        # Optional: publish all states together
        publish(overall_state)

        print("-" * 30)
        time.sleep(0.5)

finally:
    GPIO.cleanup()