from shared import *
from server.common import *

state = State(mqtt, on_error)

state.process_request(Request.POWER_ON)
assert(state.powered_on == True)


state.process_request(Request.POWER_OFF)
assert(state.powered_on == False)
