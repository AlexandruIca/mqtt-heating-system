#import paho.mqtt.client as mqtt
from common import *
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = HOST
app.config['MQTT_BROKER_PORT'] = PORT
app.config['MQTT_KEEPALIVE'] = KEEPALIVE
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

generate_temp_water_values('temperature_usage.txt', datetime.date.today().month, datetime.date.today().year, 18, 30)
generate_temp_water_values('water_temperature_usage.txt', datetime.date.today().month, datetime.date.today().year, 20, 90)

def on_error(payload):
    print(f"`on_error` called in main!!! Something went wrong: {payload}")

def jsonify(value, error):
    if error:
        return '{"value": "' + str(value) + '", "error": "' + str(error) + '"}'
    return '{"value": "' + str(value) + '"}'


@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe(f'{POWER_TOPIC}/#')
    client.subscribe(f'{TEMP_TOPIC}/#')
    client.subscribe(f'{WATER_TEMP_TOPIC}/#')
    client.subscribe(f'{STATISTICS_GET_TOPIC}/#')
    client.subscribe(f'{SCHEDULE_TEMP_TOPIC}/#')


state = State(mqtt, on_error)
error_message = ''


@mqtt.on_message()
def on_message(client, userdata, msg):
    (req, payload) = payload_to_request(msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(f'Event: {msg.topic}, {req}'), payload=payload)


@app.route('/docs')
def docs():
    return redirect('/static/index.html')

@app.route('/temperature_up', methods=['POST'])
def temperature_up():
    global error_message
    err = state.process_request(Request.TEMPERATURE_UP)
    error_message = err
    return jsonify(state.temperature, err)


@app.route('/temperature_down', methods=['POST'])
def temperature_down():
    global error_message
    err = state.process_request(Request.TEMPERATURE_DOWN)
    error_message = err
    return jsonify(state.temperature, err)


@app.route('/water_temperature_up', methods=['POST'])
def water_temperature_up():
    global error_message
    err = state.process_request(Request.WATER_TEMPERATURE_UP)
    error_message = err
    return jsonify(state.water_temperature, err)


@app.route('/water_temperature_down', methods=['POST'])
def water_temperature_down():
    global error_message
    err = state.process_request(Request.WATER_TEMPERATURE_DOWN)
    error_message = err
    return jsonify(state.water_temperature, err)

def default_callback():
    pass

@app.route('/schedule_temp', methods=['POST'])
def schedule_temp():
    global error_message
    error_message = state.process_request(Request.SCHEDULE_TEMP, default_callback, request.data)
    return state.schedule


@app.route('/')
@app.route('/index')
def index():
    global error_message
    return render_template('index.html', temperature=state.temperature, water=state.water_temperature, schedule=state.schedule, error_msg=error_message, HOST=HOST, PORT=FLASK_PORT)


@app.route('/power/<string:kind>')
def power_on(kind):
    if kind != 'on' and kind != 'off':
        return "<p>Invalid URL, expected /power/on or /power/off</p>"

    req = Request.POWER_ON if kind == 'on' else Request.POWER_OFF
    state.process_request(req, callback=lambda: print('Power on from HTTP!'))
    return f"<p>Powered {kind}: {state.powered_on}</p>"


@app.route('/temperature_usage')
def temperature_usage():
    temp_usage = state.temperature_usage
    return f"<p> Medium heat temperature used in {temp_usage[1]} is: {round(sum(temp_usage[0]) / len(temp_usage[0]))}</p>"

@app.route('/water_temperature_usage')
def water_temperature_usage():
    water_temp_usage = state.water_temperature_usage
    return f"<p> Medium water temperature used in {water_temp_usage[1]} is: {round(sum(water_temp_usage[0]) / len(water_temp_usage[0]))}</p>"


app.run()
