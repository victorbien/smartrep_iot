# MQTT
OPENAI_API_KEY=""
TB_PI1_TOKEN=""
TB_PI2_TOKEN=""
TB_BROKER="mqtt.thingsboard.cloud"
TB_PORT=1883
MQTT_TOPIC = "v1/devices/me/telemetry"


#Max Sets and Reps
NO_OF_MAX_SETS = 1
NO_OF_MAX_REPS = 3

#Equipment Name
DUMBBELL_LEFT = "dumbbell_left"
DUMBBELL_RIGHT = "dumbbell_right"
DUMBBELL_PAIR = "dumbbell_pair"
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
EXERCISE = "exercise"
SETS = "sets"
REPS_PER_SET = "reps_per_set"
BAD_REPS = "bad_reps"
FORM_SCORE = "form_score"
ANGLE_DATA = "angle_data"
STAGE = "stage"
CURRENT_REPS = "current_reps"
CURRENT_REP_ANGLES = "current_rep_angles"
REP_EVENTS = "rep_events"
MOTION_SCORE = "motion_score"
TARGET_REACHED_LOGGED = "target_reached_logged"
COACHING_SUMMARY = "coaching_summary"


# PCF8591
PCF_ADDRESS = 0x48


#Sleep Time
SLEEP_TIME = 0.5


#Supported Exercises
BICEP_CURL = "bicep_curl"
SQUAT = "squat"


# Equipment mapping
EQUIPMENT = {
    DUMBBELL_LEFT: {CHANNEL: 0, THRESHOLD: 100, LED_GREEN: 18, LED_RED: 17},
    DUMBBELL_RIGHT: {CHANNEL: 1, THRESHOLD: 100, LED_GREEN: 27, LED_RED: 22},
    FOAM_ROLLER: {CHANNEL: 2, THRESHOLD: 100, LED_GREEN: 24, LED_RED: 23},
    CHAIR: {CHANNEL: 3, THRESHOLD: 100, LED_GREEN: 5, LED_RED: 6},
}

