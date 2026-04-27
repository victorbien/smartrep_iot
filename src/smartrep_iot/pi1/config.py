# MQTT
OPENAI_API_KEY="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"
TB_PI1_TOKEN="Nyj11kX9rElJ7sUGhvDO"
TB_PI2_TOKEN="gmvlMY1g7xVRYlfDQvKQ"
TB_BROKER="mqtt.thingsboard.cloud"
TB_PORT=1883
MQTT_TOPIC = "v1/devices/me/telemetry"

#Equipment Name
DUMBBELL_LEFT = "dumbbell_left"
DUMBBELL_RIGHT = "dumbbell_right"
FOAM_ROLLER = "foam_roller"
CHAIR = "chair"

#Equipment Attributes
CHANNEL = "channel"
THRESHOLD = "threshold"
LED_GREEN = "led_green"
LED_RED = "led_red"

#Equipment Status
AVAILABLE = "available"
OCCUPIED = "occupied"

#Session Variables
EVENT = "event"
EQUIPMENT_NAME = "equipment"
SESSION_ID = "session_id"
START_TIME = "start_time"
END_TIME = "end_time"
SESSION_DURATION = "session_duration_s"

# PCF8591
PCF_ADDRESS = 0x48

#Sleep Time
SLEEP_TIME = 0.5

# Equipment mapping
EQUIPMENT = {
    DUMBBELL_LEFT: {CHANNEL: 0, THRESHOLD: 100, LED_GREEN: 18, LED_RED: 17},
    DUMBBELL_RIGHT: {CHANNEL: 1, THRESHOLD: 100, LED_GREEN: 27, LED_RED: 22},
    FOAM_ROLLER: {CHANNEL: 2, THRESHOLD: 100, LED_GREEN: 24, LED_RED: 23},
    CHAIR: {CHANNEL: 3, THRESHOLD: 100, LED_GREEN: 5, LED_RED: 6},
}

