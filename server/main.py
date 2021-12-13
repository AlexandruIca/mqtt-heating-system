import paho.mqtt.client as mqtt
from common import *

state = State()


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{POWER_TOPIC}/#')
    client.subscribe(f'{TEMP_TOPIC}/#')


def on_message(client, userdata, msg):
    req = payload_to_request(msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(f'Event: {msg.topic}, {req}'))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, KEEPALIVE)

client.loop_forever()
