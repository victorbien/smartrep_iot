import paho.mqtt.client as mqtt
import json
from config import THINGSBOARD_HOST, ACCESS_TOKEN

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)


def publish(payload):
    client.publish("v1/devices/me/telemetry", json.dumps(payload))