from enum import Enum

HOST: str = 'localhost'
PORT: int = 1883
KEEPALIVE: int = 60

POWER_TOPIC: str = 'power'
TEMP_TOPIC: str = 'temperature'
WATER_TEMP_TOPIC: str = 'water_temperature'


class Request(Enum):
    INVALID = 0
    POWER_ON = 1
    POWER_OFF = 2
    TEMPERATURE_UP = 3
    TEMPERATURE_DOWN = 4
    WATER_TEMPERATURE_UP = 5
    WATER_TEMPERATURE_DOWN = 6

def on_power_request(state, status, f):
    state.powered_on = status
    f()

def on_change_temperature_request(state, f, sign, how_much):
    if sign == '+':
        state.temperature += how_much
    elif sign == '-':
        state.temperature -= how_much
    f()

def on_change_water_temperature_request(state, f, sign, how_much):
    if sign == '+':
        state.water_temperature += how_much
    elif sign == '-':
        state.water_temperature -= how_much
    f()

request_map = {
    Request.INVALID: lambda _, f: f(),
    Request.POWER_ON: lambda state, f: on_power_request(state, True, f),
    Request.POWER_OFF: lambda state, f: on_power_request(state, False, f),
    Request.TEMPERATURE_UP: lambda state, f: on_change_temperature_request(state, f, '+', 0.5),
    Request.TEMPERATURE_DOWN: lambda state, f: on_change_temperature_request(state, f, '-', 0.5),
    Request.WATER_TEMPERATURE_UP: lambda state, f: on_change_water_temperature_request(state, f, '+', .5),
    Request.WATER_TEMPERATURE_DOWN: lambda state, f: on_change_water_temperature_request(state, f, '-', -.5),
}


def payload_to_request(topic: str, payload: str):
    if topic == POWER_TOPIC:
        if payload == 'on':
            return Request.POWER_ON
        elif payload == 'off':
            return Request.POWER_OFF
        else:
            return Request.INVALID
    elif topic == TEMP_TOPIC:
        if payload == 'up':
            return Request.TEMPERATURE_UP
        elif payload == 'down':
            return Request.TEMPERATURE_DOWN
    elif topic == WATER_TEMP_TOPIC:
        if payload == 'up':
            return Request.WATER_TEMPERATURE_UP
        elif payload == 'down':
            return Request.WATER_TEMPERATURE_DOWN
    else:
        return Request.INVALID


def request_to_payload(req: Request):
    if req == Request.POWER_ON:
        return (POWER_TOPIC, 'on')
    elif req == Request.POWER_OFF:
        return (POWER_TOPIC, 'off')
    elif req == Request.TEMPERATURE_UP:
        return (TEMP_TOPIC, 'up')
    elif req == Request.TEMPERATURE_DOWN:
        return (TEMP_TOPIC, 'down')
    elif req == Request.WATER_TEMPERATURE_UP:
        return (WATER_TEMP_TOPIC, 'up')
    elif req == Request.WATER_TEMPERATURE_DOWN:
        return (WATER_TEMP_TOPIC, 'down')


def default_callback():
    pass


class State:
    def __init__(self):
        self.powered_on = False
        self.temperature = 20 
        self.water_temperature = 20

    def process_request(self, req: Request, callback=default_callback):
        request_map[req](self, callback)
        print(self.temperature)