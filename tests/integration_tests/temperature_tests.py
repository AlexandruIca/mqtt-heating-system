from shared import post_to

output = 0
for i in range(100):
    output = float(post_to('temperature_up'))

assert(output == 30)

for i in range(100):
    output = float(post_to('temperature_down'))


assert(output == 18)
