from enum import Enum
import random, datetime, calendar, json

HOST: str = '127.0.0.1'
PORT: int = 1883
FLASK_PORT: int = 5000
KEEPALIVE: int = 60
SEEDS = {calendar.month_name[i]: i ** 5 for i in range(1, 13)}

POWER_TOPIC: str = 'power'
TEMP_TOPIC: str = 'temperature'
WARNINGS_TOPIC: str = 'warning'
TEMP_WARNINGS_SUBTOPIC: str = 'temperature'
WATER_TEMP_TOPIC: str = 'water_temperature'
STATISTICS_GET_TOPIC: str = 'statistics_get'
STATISTICS_SET_TOPIC: str = 'statistics_set'
WATER_USAGE_SUBTOPIC: str = 'water'
GAS_USAGE_SUBTOPIC: str = 'gas'
SCHEDULE_TEMP_TOPIC: str = 'schedule_temp'


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
    SCHEDULE_TEMP = 10


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

def on_schedule_request(state, f, payload):
    parsedPayload = json.loads(payload)
    if int(parsedPayload['start_hour']) < 0 or  int(parsedPayload['start_hour']) > 23 or int(parsedPayload['stop_hour']) < 0 or int(parsedPayload['stop_hour']) > 23:
        state.client.publish(
            f'{WARNINGS_TOPIC}', "Invalid hour scheduling")
        return "Invalid hour scheduling"
    if int(parsedPayload['scheduled_temp']) > 30:
        state.client.publish(
            f'{WARNINGS_TOPIC}', "High Temperature Requested")
        return "High temperature requested"

    if int(parsedPayload['scheduled_temp']) < 18:
        state.client.publish(
            f'{WARNINGS_TOPIC}', "Minimum Temperature Requested")
        return "Minimum temperature requested"


    new_intervals_for_day = []
    for interval in state.schedule[parsedPayload['day']]:
        # print(interval[1] <= int(payload['stop_hour']))
        if interval[0] <= int(parsedPayload['start_hour']) <= interval[1] and interval[1] <= int(parsedPayload['stop_hour']):
            new_intervals_for_day.append([interval[0], int(parsedPayload['start_hour']), interval[2]])
            new_intervals_for_day.append([int(parsedPayload['start_hour']), interval[1], int(parsedPayload['scheduled_temp'])])
        elif interval[0] <= int(parsedPayload['stop_hour']) <= interval[1] and interval[0] >= int(parsedPayload['start_hour']):
            new_intervals_for_day.append([interval[0], int(parsedPayload['stop_hour']), int(parsedPayload['scheduled_temp'])])
            new_intervals_for_day.append([int(parsedPayload['stop_hour']), interval[1], interval[2]])
        elif interval[0] <= int(parsedPayload['start_hour']) <= interval[1] and interval[0] <= int(parsedPayload['stop_hour']) <= interval[1]:
            new_intervals_for_day.append([interval[0], int(parsedPayload['start_hour']), interval[2]])
            new_intervals_for_day.append([int(parsedPayload['start_hour']), int(parsedPayload['stop_hour']), int(parsedPayload['scheduled_temp'])])
            new_intervals_for_day.append([int(parsedPayload['stop_hour']), interval[1], interval[2]])
        else:
            new_intervals_for_day.append(interval)

    state.schedule[parsedPayload['day']] = new_intervals_for_day
    f()


request_map = {
    Request.INVALID: lambda _1, _2, f: f(),
    Request.POWER_ON: lambda state, _, f: on_power_request(state, True, f),
    Request.POWER_OFF: lambda state, _, f: on_power_request(state, False, f),
    Request.TEMPERATURE_UP: lambda state, _, f: on_change_temperature_request(state, f, '+', 0.5),
    Request.TEMPERATURE_DOWN: lambda state, _, f: on_change_temperature_request(state, f, '-', 0.5),
    Request.WARNING: lambda state, payload, f: state.on_error(payload),
    Request.WATER_TEMPERATURE_UP: lambda state, _, f: on_change_water_temperature_request(state, f, '+', .5),
    Request.WATER_TEMPERATURE_DOWN: lambda state, _, f: on_change_water_temperature_request(state, f, '-', .5),
    Request.WATER_STATISTICS: lambda state, _, f: on_statistics(state, f, 'water'),
    Request.GAS_STATISTICS: lambda state, _, f: on_statistics(state, f, 'gas'),
    Request.SCHEDULE_TEMP: lambda state, payload, f: on_schedule_request(state, f, payload)
}


def payload_to_request(topic: str, payload: str):
    if topic == POWER_TOPIC:
        if payload == 'on':
            return (Request.POWER_ON,)
        elif payload == 'off':
            return (Request.POWER_OFF,)
        else:
            return (Request.INVALID,)
    elif topic.startswith(TEMP_TOPIC):
        if payload == 'up':
            return (Request.TEMPERATURE_UP,)
        elif payload == 'down':
            return (Request.TEMPERATURE_DOWN,)
    elif topic.startswith(WARNINGS_TOPIC):
        return (Request.WARNING,)
    elif topic == WATER_TEMP_TOPIC:
        if payload == 'up':
            return (Request.WATER_TEMPERATURE_UP,)
        elif payload == 'down':
            return (Request.WATER_TEMPERATURE_DOWN,)
    elif topic.startswith(f'{STATISTICS_GET_TOPIC}/{WATER_USAGE_SUBTOPIC}'):
        return (Request.WATER_STATISTICS,)
    elif topic.startswith(f'{STATISTICS_GET_TOPIC}/{GAS_USAGE_SUBTOPIC}'):
        return (Request.GAS_STATISTICS,)
    elif topic == SCHEDULE_TEMP_TOPIC:
        return (Request.SCHEDULE_TEMP, payload)
    else:
        return (Request.INVALID,)


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
    elif req == Request.SCHEDULE_TEMP:
        return (SCHEDULE_TEMP_TOPIC, payload)


def default_callback():
    pass


def generate_temp_water_values(file_name, month, year, minimum, maximum):
    num_days = calendar.monthrange(year, month)[1]
    random.seed(SEEDS[calendar.month_name[datetime.date.today().month]])
    with open(file_name, 'w') as f:
        for i in range(num_days):
            f.write(str(random.randint(minimum, maximum)) + "\n")

def read_temp_water_values(file_name):
    common = []
    with open(file_name) as f:
        line = f.readline()
        common.append(int(line))
        while line:
            line = f.readline()
            if line != '':
                common.append(int(line))
    return (common, calendar.month_name[datetime.date.today().month])

class State:
    def __init__(self, client, on_error):
        self.powered_on = False
        self.temperature = 20
        self.water_temperature = 20
        self.client = client
        self.on_error = on_error
        self.temperature_usage = read_temp_water_values('temperature_usage.txt')
        self.water_temperature_usage = read_temp_water_values('water_temperature_usage.txt')

        self.schedule = {
            "mon": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "tue": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "wed": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "thu": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "fri": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "sat": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
            "sun": [[0, 9, 20], [9, 22, 25], [22, 0, 20]],
        }

    def process_request(self, req: Request, callback=default_callback, payload=None):
        return request_map[req](self, payload, callback)
