import paho.mqtt.client as mqtt
from common import *


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{POWER_TOPIC}/#')


def on_message(client, userdata, msg):
    payload = msg.payload.decode('ASCII')

    if msg.topic == POWER_TOPIC:
        print(f'Power request: {payload}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, KEEPALIVE)

client.loop_forever()
