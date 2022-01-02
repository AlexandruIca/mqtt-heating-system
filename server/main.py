#import paho.mqtt.client as mqtt
from common import *
from flask import Flask, redirect, url_for, render_template
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


state = State(mqtt, on_error)

@mqtt.on_message()
def on_message(client, userdata, msg):
    req = payload_to_request(msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(f'Event: {msg.topic}, {req}'))


@app.route('/temperature_up')
def temperature_up():
    state.process_request(Request.TEMPERATURE_UP)
    return redirect(url_for('index'))

@app.route('/temperature_down')
def temperature_down():
    state.process_request(Request.TEMPERATURE_DOWN)
    return redirect(url_for('index'))
    

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', temperature = state.temperature)

@app.route('/power/<string:kind>')
def power_on(kind):
    if kind != 'on' and kind != 'off':
        return "<p>Invalid URL, expected /power/on or /power/off</p>"

    req = Request.POWER_ON if kind == 'on' else Request.POWER_OFF
    state.process_request(req, callback=lambda: print('Power on from HTTP!'))
    return f"<p>Powered {kind}: {state.powered_on}</p>"


app.run()
