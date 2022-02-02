from shared import post_to


result = None
output = 0


for i in range(100):
    result = post_to('water_temperature_up')
    assert(result['type'] == 'number')

    if 'error' in result and len(result['error']) > 0:
        break

    output = float(result['value'])


assert(output == 90)


for i in range(200):
    result = post_to('water_temperature_down')
    assert(result['type'] == 'number')

    if 'error' in result and len(result['error']) > 0:
        break

    output = float(result['value'])


assert(output == 20)
