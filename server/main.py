import datetime
from common import *
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask_mqtt import Mqtt
import json
import apscheduler

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = HOST
app.config['MQTT_BROKER_PORT'] = PORT
app.config['MQTT_KEEPALIVE'] = KEEPALIVE
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)


generate_temp_water_values('temperature_usage.txt', datetime.date.today(
).month, datetime.date.today().year, MIN_GAS_TEMP, MAX_GAS_TEMP)
generate_temp_water_values('water_temperature_usage.txt', datetime.date.today(
).month, datetime.date.today().year, MIN_WATER_TEMP, MAX_WATER_TEMP)


def on_error(payload):
    print(f"`on_error` called in main!!! Something went wrong: {payload}")


def jsonify(msg_type, value, error):
    if error:
        return json.dumps({"type": msg_type, "value": value, "error": error})
    return json.dumps({"type": msg_type, "value": value})


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
    (req, req_payload) = payload_to_request(
        msg.topic, msg.payload.decode('ASCII'))
    state.process_request(req, lambda: print(
        f'Event: {msg.topic}, {req}'), payload=req_payload)


@app.route('/docs')
def docs():
    return redirect('/static/index.html')


@app.route('/temperature_up', methods=['POST'])
def temperature_up():
    global error_message
    error_message = state.process_request(Request.TEMPERATURE_UP)
    return jsonify("number", state.temperature, error_message)


@app.route('/temperature_down', methods=['POST'])
def temperature_down():
    global error_message
    error_message = state.process_request(Request.TEMPERATURE_DOWN)
    return jsonify("number", state.temperature, error_message)


@app.route('/water_temperature_up', methods=['POST'])
def water_temperature_up():
    global error_message
    error_message = state.process_request(Request.WATER_TEMPERATURE_UP)
    return jsonify("number", state.water_temperature, error_message)


@app.route('/water_temperature_down', methods=['POST'])
def water_temperature_down():
    global error_message
    error_message = state.process_request(Request.WATER_TEMPERATURE_DOWN)
    return jsonify("number", state.water_temperature, error_message)


def default_callback():
    pass


@app.route('/schedule_temp', methods=['POST'])
def schedule_temp():
    global error_message
    error_message = state.process_request(
        Request.SCHEDULE_TEMP, default_callback, request.data)
    return jsonify("schedule", state.schedule, error_message)


@app.route('/')
@app.route('/index')
def index():
    global error_message
    return render_template('index.html', temperature=state.temperature, water=state.water_temperature, schedule=state.schedule, error_msg=error_message, HOST=HOST, PORT=FLASK_PORT)


@app.route('/power/<string:kind>', methods=['POST'])
def power_on(kind):
    global error_message
    if kind != 'on' and kind != 'off':
        return "Invalid URL, expected /power/on or /power/off"

    req = Request.POWER_ON if kind == 'on' else Request.POWER_OFF
    error_message = state.process_request(
        req, callback=lambda: print('Power on from HTTP!'))
    return jsonify('power', str(state.powered_on), error_message)


@app.route('/temperature_usage', methods=['POST'])
def temperature_usage():
    temp_usage = state.temperature_usage
    return jsonify('statistics', {"month": temp_usage[1], "average_usage": round(sum(temp_usage[0]) / len(temp_usage[0]))}, "")


@app.route('/water_temperature_usage', methods=['POST'])
def water_temperature_usage():
    water_temp_usage = state.water_temperature_usage
    return jsonify('statistics', {"month": water_temp_usage[1], "average_usage": round(sum(water_temp_usage[0]) / len(water_temp_usage[0]))}, "")


def background_schedule():
    week_day = datetime.date.today().weekday()
    hour = datetime.datetime.now().hour

    days = {0: 'mon', 1: 'tue', 2: 'wed',
            3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
    day_schedule = state.schedule[days[week_day]]

    schedule = dict((hour, i[2]) for hour in range(0, 24) for i in day_schedule if (
        i[0] <= hour < i[1]) or (i[1] == 0 and i[0] <= hour))
    current_temp = schedule[hour]

    if state.powered_on:
        state.temperature = current_temp


state.scheduler.add_job(background_schedule, 'interval', minutes=1)
app.run()
