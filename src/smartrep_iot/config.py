# MQTT
OPENAI_API_KEY="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"
TB_PI1_TOKEN="Nyj11kX9rElJ7sUGhvDO"
TB_PI2_TOKEN="gmvlMY1g7xVRYlfDQvKQ"
TB_BROKER="mqtt.thingsboard.cloud"
TB_PORT=1883

# PCF8591
PCF_ADDRESS = 0x48

# Equipment mapping
EQUIPMENT = {
    "dumbbell_left": {"channel": 0, "threshold": 100, "led_green": 18, "led_red": 17},
    "dumbbell_right": {"channel": 1, "threshold": 100, "led_green": 27, "led_red": 22},
    "foam_roller": {"channel": 2, "threshold": 90, "led_green": 24, "led_red": 23},
    "chair": {"channel": 3, "threshold": 110, "led_green": 5, "led_red": 6},
}
