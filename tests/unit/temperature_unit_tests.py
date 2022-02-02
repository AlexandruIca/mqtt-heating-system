from shared import *
from server.common import *


state = State(mqtt, on_error)


for i in range(40):
    state.process_request(Request.TEMPERATURE_UP)


assert(state.temperature == MAX_GAS_TEMP)


for i in range(90):
    state.process_request(Request.TEMPERATURE_DOWN)


assert(state.temperature == MIN_GAS_TEMP)
