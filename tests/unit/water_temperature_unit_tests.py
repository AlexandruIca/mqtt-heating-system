from shared import *
from server.common import *


state = State(mqtt, on_error)


for i in range(100):
    state.process_request(Request.WATER_TEMPERATURE_UP)


assert(state.water_temperature == MAX_WATER_TEMP)


for i in range(200):
    state.process_request(Request.WATER_TEMPERATURE_DOWN)


assert(state.water_temperature == MIN_WATER_TEMP)
