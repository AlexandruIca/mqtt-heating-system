import time
import paho.mqtt.client as mqtt
from common import *


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{WARNINGS_TOPIC}/#')
    client.subscribe(f'{SCHEDULE_TEMP_TOPIC}/#')
    test_payload = {
        "day": "mon",
        "start_hour": "7",
        "stop_hour": "8",
        "scheduled_temp": "25"
    }
    (topic, payload) = request_to_payload(
        Request.SCHEDULE_TEMP, payload=json.dumps(test_payload))
    client.publish(topic, payload)


def on_message(client, userdata, msg):
    print(f'Received PUBLISH: topic={msg.topic}, payload: {msg.payload}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(HOST, PORT, KEEPALIVE)
client.loop_start()
time.sleep(1)
client.loop_stop(force=False)
