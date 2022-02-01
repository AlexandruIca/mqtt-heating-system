import paho.mqtt.client as mqtt
from common import *


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{WARNINGS_TOPIC}/#')
    client.subscribe(f'{STATISTICS_SET_TOPIC}/#')
    (topic, payload) = request_to_payload(Request.WATER_STATISTICS)
    client.publish(topic, payload)
    (topic, payload) = request_to_payload(Request.GAS_STATISTICS)
    client.publish(topic, payload)


def on_message(client, userdata, msg):
    print(f'Received PUBLISH: topic={msg.topic}, payload: {msg.payload}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, KEEPALIVE)

client.loop_forever()
