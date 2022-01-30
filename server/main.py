#import paho.mqtt.client as mqtt
from common import *
from flask import Flask, redirect, url_for, render_template, send_from_directory
from flask_mqtt import Mqtt


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = HOST
app.config['MQTT_BROKER_PORT'] = PORT
app.config['MQTT_KEEPALIVE'] = KEEPALIVE
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)


def on_error(payload):
    print(f"`on_error` called in main!!! Something went wrong: {payload}")


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{POWER_TOPIC}/#')
    client.subscribe(f'{TEMP_TOPIC}/#')
    client.subscribe(f'{WATER_TEMP_TOPIC}/#')
    client.subscribe(f'{STATISTICS_GET_TOPIC}/#')


state = State(mqtt, on_error)
error_message = ''


@mqtt.on_message()
def on_message(client, userdata, msg):
    req = payload_to_request(msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(f'Event: {msg.topic}, {req}'))


@app.route('/temperature_up', methods=['POST'])
def temperature_up():
    global error_message
    error_message = state.process_request(Request.TEMPERATURE_UP)
    return str(state.temperature)


@app.route('/temperature_down', methods=['POST'])
def temperature_down():
    global error_message
    error_message = state.process_request(Request.TEMPERATURE_DOWN)
    return str(state.temperature)


@app.route('/water_temperature_up', methods=['POST'])
def water_temperature_up():
    global error_message
    error_message = state.process_request(Request.WATER_TEMPERATURE_UP)
    return str(state.water_temperature)


@app.route('/water_temperature_down', methods=['POST'])
def water_temperature_down():
    global error_message
    error_message = state.process_request(Request.WATER_TEMPERATURE_DOWN)
    return str(state.water_temperature)


@app.route('/')
@app.route('/index')
def index():
    global error_message
    return render_template('index.html', temperature=state.temperature, water=state.water_temperature, error_msg=error_message, HOST=HOST, PORT=FLASK_PORT)


@app.route('/power/<string:kind>')
def power_on(kind):
    if kind != 'on' and kind != 'off':
        return "<p>Invalid URL, expected /power/on or /power/off</p>"

    req = Request.POWER_ON if kind == 'on' else Request.POWER_OFF
    state.process_request(req, callback=lambda: print('Power on from HTTP!'))
    return f"<p>Powered {kind}: {state.powered_on}</p>"


app.run()
