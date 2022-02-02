from shared import post_to


result = post_to('temperature_usage')
assert(result['type'] == 'statistics')
assert('average_usage' in result['value'])


result = post_to('water_temperature_usage')
assert(result['type'] == 'statistics')
assert('average_usage' in result['value'])
