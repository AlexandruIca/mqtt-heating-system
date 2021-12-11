from enum import Enum

HOST: str = 'localhost'
PORT: int = 1883
KEEPALIVE: int = 60

POWER_TOPIC: str = 'power'


class Request(Enum):
    INVALID = 0
    POWER_ON = 1
    POWER_OFF = 2


def on_power_request(state, status, f):
    state.powered_on = status
    f()


request_map = {
    Request.INVALID: lambda _, f: f(),
    Request.POWER_ON: lambda state, f: on_power_request(state, True, f),
    Request.POWER_OFF: lambda state, f: on_power_request(state, False, f),
}


def payload_to_request(topic: str, payload: str):
    if topic == POWER_TOPIC:
        if payload == 'on':
            return Request.POWER_ON
        elif payload == 'off':
            return Request.POWER_OFF
        else:
            return Request.INVALID
    else:
        return Request.INVALID


def request_to_payload(req: Request):
    if req == Request.POWER_ON:
        return (POWER_TOPIC, 'on')
    elif req == Request.POWER_OFF:
        return (POWER_TOPIC, 'off')


def default_callback():
    pass


class State:
    def __init__(self):
        self.powered_on = False

    def process_request(self, req: Request, callback=default_callback):
        request_map[req](self, callback)
