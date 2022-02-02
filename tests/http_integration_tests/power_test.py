from shared import post_to


result = post_to('/power/on')
assert(result['type'] == 'power')
assert(result['value'] == 'True')


result = post_to('/power/off')
assert(result['type'] == 'power')
assert(result['value'] == 'False')


result = post_to('/temperature_up')
assert(result['type'] == 'number')
assert(len(result['error']) > 0)


result = post_to('/power/on')
assert(result['type'] == 'power')
assert(result['value'] == 'True')
