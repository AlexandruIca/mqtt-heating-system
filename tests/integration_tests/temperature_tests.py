from shared import post_to


result = None
output = 0


for i in range(100):
    result = post_to('temperature_up')
    assert(result['type'] == 'number')

    if 'error' in result and len(result['error']) > 0:
        break

    output = float(result['value'])


assert(output == 30)


for i in range(100):
    result = post_to('temperature_down')
    assert(result['type'] == 'number')

    if 'error' in result and len(result['error']) > 0:
        break

    output = float(result['value'])


assert(output == 18)
