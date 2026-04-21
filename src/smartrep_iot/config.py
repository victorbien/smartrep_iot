# MQTT
THINGSBOARD_HOST = "mqtt.thingsboard.cloud"
ACCESS_TOKEN = "YOUR_PI1_ACCESS_TOKEN"

# PCF8591
PCF_ADDRESS = 0x48

# Equipment mapping
EQUIPMENT = {
    "dumbbell_left": {"channel": 0, "threshold": 100, "led_green": 18, "led_red": 17},
    "dumbbell_right": {"channel": 1, "threshold": 100, "led_green": 27, "led_red": 22},
    "foam_roller": {"channel": 2, "threshold": 90, "led_green": 24, "led_red": 23},
    "chair": {"channel": 3, "threshold": 110, "led_green": 5, "led_red": 6},
}