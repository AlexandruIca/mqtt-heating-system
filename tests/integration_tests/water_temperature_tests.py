from shared import post_to

output = 0
for i in range(100):
    output = float(post_to('water_temperature_up'))

assert(output == 90)

for i in range(200):
    output = float(post_to('water_temperature_down'))


assert(output == 20)
