#import paho.mqtt.client as mqtt
from common import *
from flask import Flask
from flask_mqtt import Mqtt


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = HOST
app.config['MQTT_BROKER_PORT'] = PORT
app.config['MQTT_KEEPALIVE'] = KEEPALIVE
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)


def on_error(topic, payload):
    print("on_error called in main!!! Something went wrong!")


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{POWER_TOPIC}/#')
    client.subscribe(f'{TEMP_TOPIC}/#')
    client.subscribe(f'{WATER_TEMP_TOPIC}/#')
    client.subscribe(f'{STATISTICS_GET_TOPIC}/#')


@mqtt.on_message()
def on_message(client, userdata, msg):
    req = payload_to_request(msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(f'Event: {msg.topic}, {req}'))


state = State(mqtt, on_error)
app.run()
