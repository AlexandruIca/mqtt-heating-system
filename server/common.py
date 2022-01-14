from enum import Enum

HOST: str = '127.0.0.1'
PORT: int = 1883
FLASK_PORT: int = 5000
KEEPALIVE: int = 60

POWER_TOPIC: str = 'power'
TEMP_TOPIC: str = 'temperature'
WARNINGS_TOPIC: str = 'warning'
TEMP_WARNINGS_SUBTOPIC: str = 'temperature'
WATER_TEMP_TOPIC: str = 'water_temperature'
STATISTICS_GET_TOPIC: str = 'statistics_get'
STATISTICS_SET_TOPIC: str = 'statistics_set'
WATER_USAGE_SUBTOPIC: str = 'water'
GAS_USAGE_SUBTOPIC: str = 'gas'


class Request(Enum):
    INVALID = 0
    POWER_ON = 1
    POWER_OFF = 2
    TEMPERATURE_UP = 3
    TEMPERATURE_DOWN = 4
    WARNING = 5
    WATER_TEMPERATURE_UP = 6
    WATER_TEMPERATURE_DOWN = 7
    WATER_STATISTICS = 8
    GAS_STATISTICS = 9


def on_power_request(state, status, f):
    state.powered_on = status
    f()


def on_change_temperature_request(state, f, sign, how_much):
    if sign == '+':
        if state.temperature + how_much > 30:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "High Temperature Reached")
            return "High temperature reached"
        else:
            state.temperature += how_much
    elif sign == '-':
        if state.temperature - how_much < 18:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "Minimum Temperature Reached")
            return "Minimum temperature reached"
        else:
            state.temperature -= how_much
    f()


def on_change_water_temperature_request(state, f, sign, how_much):
    if sign == '+':
        if state.water_temperature + how_much > 90:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "High Water Temperature Reached")
            return "High water temperature reached"
        else:
            state.water_temperature += how_much
    elif sign == '-':
        if state.water_temperature - how_much < 20:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "Low Water Temperature Reached")
            return "Low water temperature reached"
        else:
            state.water_temperature -= how_much
    f()


def on_statistics(state, f, stat_type):
    if stat_type == 'water':
        state.client.publish(
            f'{STATISTICS_SET_TOPIC}/{WATER_USAGE_SUBTOPIC}', str(state.water_usage))
    elif stat_type == 'gas':
        state.client.publish(
            f'{STATISTICS_SET_TOPIC}/{GAS_USAGE_SUBTOPIC}', str(state.gas_usage))
    f()


request_map = {
    Request.INVALID: lambda _1, _2, f: f(),
    Request.POWER_ON: lambda state, _, f: on_power_request(state, True, f),
    Request.POWER_OFF: lambda state, _, f: on_power_request(state, False, f),
    Request.TEMPERATURE_UP: lambda state, _, f: on_change_temperature_request(state, f, '+', 0.5),
    Request.TEMPERATURE_DOWN: lambda state, _, f: on_change_temperature_request(state, f, '-', 0.5),
    Request.WARNING: lambda state, payload, f: state.on_error(topic, payload),
    Request.WATER_TEMPERATURE_UP: lambda state, _, f: on_change_water_temperature_request(state, f, '+', .5),
    Request.WATER_TEMPERATURE_DOWN: lambda state, _, f: on_change_water_temperature_request(state, f, '-', .5),
    Request.WATER_STATISTICS: lambda state, _, f: on_statistics(state, f, 'water'),
    Request.GAS_STATISTICS: lambda state, _, f: on_statistics(state, f, 'gas'),
}


def payload_to_request(topic: str, payload: str):
    if topic == POWER_TOPIC:
        if payload == 'on':
            return Request.POWER_ON
        elif payload == 'off':
            return Request.POWER_OFF
        else:
            return Request.INVALID
    elif topic.startswith(TEMP_TOPIC):
        if payload == 'up':
            return Request.TEMPERATURE_UP
        elif payload == 'down':
            return Request.TEMPERATURE_DOWN
    elif topic.startswith(WARNINGS_TOPIC):
        return Request.WARNING
    elif topic == WATER_TEMP_TOPIC:
        if payload == 'up':
            return Request.WATER_TEMPERATURE_UP
        elif payload == 'down':
            return Request.WATER_TEMPERATURE_DOWN
    elif topic.startswith(f'{STATISTICS_GET_TOPIC}/{WATER_USAGE_SUBTOPIC}'):
        return Request.WATER_STATISTICS
    elif topic.startswith(f'{STATISTICS_GET_TOPIC}/{GAS_USAGE_SUBTOPIC}'):
        return Request.GAS_STATISTICS
    else:
        return Request.INVALID


def request_to_payload(req: Request, payload=None):
    if req == Request.POWER_ON:
        return (POWER_TOPIC, 'on')
    elif req == Request.POWER_OFF:
        return (POWER_TOPIC, 'off')
    elif req == Request.TEMPERATURE_UP:
        return (TEMP_TOPIC, 'up')
    elif req == Request.TEMPERATURE_DOWN:
        return (TEMP_TOPIC, 'down')
    elif req == Request.WARNING:
        return (WARNINGS_TOPIC, payload)
    elif req == Request.WATER_TEMPERATURE_UP:
        return (WATER_TEMP_TOPIC, 'up')
    elif req == Request.WATER_TEMPERATURE_DOWN:
        return (WATER_TEMP_TOPIC, 'down')
    elif req == Request.WATER_STATISTICS:
        return (f'{STATISTICS_GET_TOPIC}/{WATER_USAGE_SUBTOPIC}', payload)
    elif req == Request.GAS_STATISTICS:
        return (f'{STATISTICS_GET_TOPIC}/{GAS_USAGE_SUBTOPIC}', payload)


def default_callback():
    pass


class State:
    def __init__(self, client, on_error):
        self.powered_on = False
        self.temperature = 20
        self.water_temperature = 20
        self.client = client
        self.on_error = on_error
        # cata apa a consumat in ultimele x luni
        self.water_usage = [10, 50, 32, 24]
        self.gas_usage = [5, 6, 7, 8]

    def process_request(self, req: Request, callback=default_callback, payload=None):
        return request_map[req](self, payload, callback)
