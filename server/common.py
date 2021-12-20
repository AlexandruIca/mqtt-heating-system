from enum import Enum

HOST: str = 'localhost'
PORT: int = 1883
KEEPALIVE: int = 60

POWER_TOPIC: str = 'power'
TEMP_TOPIC: str = 'temperature'
WARNINGS_TOPIC: str = 'warning'
TEMP_WARNINGS_SUBTOPIC: str = 'temperature'


class Request(Enum):
    INVALID = 0
    POWER_ON = 1
    POWER_OFF = 2
    TEMPERATURE_UP = 3
    TEMPERATURE_DOWN = 4
    WARNING = 5


def on_power_request(state, status, f):
    state.powered_on = status
    f()


def on_change_temperature_request(state, f, sign, how_much):
    if sign == '+':
        if state.temperature + how_much > 30:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "High Temperature Reached")
        else:
            state.temperature += how_much
    elif sign == '-':
        if state.temperature - how_much < 18:
            state.client.publish(
                f'{WARNINGS_TOPIC}/{TEMP_WARNINGS_SUBTOPIC}', "Minimum Temperature Reached")
        else:
            state.temperature -= how_much
    f()


request_map = {
    Request.INVALID: lambda _1, _2, f: f(),
    Request.POWER_ON: lambda state, _, f: on_power_request(state, True, f),
    Request.POWER_OFF: lambda state, _, f: on_power_request(state, False, f),
    Request.TEMPERATURE_UP: lambda state, _, f: on_change_temperature_request(state, f, '+', 0.5),
    Request.TEMPERATURE_DOWN: lambda state, _, f: on_change_temperature_request(state, f, '-', 0.5),
    Request.WARNING: lambda state, payload, f: state.on_error(topic, payload),
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


def default_callback():
    pass


class State:
    def __init__(self, client, on_error):
        self.powered_on = False
        self.temperature = 20
        self.client = client
        self.on_error = on_error

    def process_request(self, req: Request, callback=default_callback, payload=None):
        request_map[req](self, payload, callback)
        print(self.temperature)
