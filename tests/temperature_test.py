import time
import paho.mqtt.client as mqtt
from common import *

i = 0


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{WARNINGS_TOPIC}/#')
    for i in range(40):
        (topic, payload) = request_to_payload(Request.TEMPERATURE_UP)
        client.publish(topic, payload)
    for i in range(90):
        (topic, payload) = request_to_payload(Request.TEMPERATURE_DOWN)
        client.publish(topic, payload)


def on_message(client, userdata, msg):
    global i
    print(
        f'Received PUBLISH: topic={msg.topic}, payload: {msg.payload}, counter: {i}')
    i += 1


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(HOST, PORT, KEEPALIVE)
client.loop_start()
time.sleep(3)
client.loop_stop(force=False)
