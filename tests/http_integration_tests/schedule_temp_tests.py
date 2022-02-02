from shared import post_to


result = post_to('schedule_temp', {
                 'day': 'mon', 'start_hour': 4, 'stop_hour': 8, 'scheduled_temp': 23})
print(result)
