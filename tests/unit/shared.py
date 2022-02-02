class Mqtt:
    def publish(topic, payload, *args):
        pass


mqtt = Mqtt()


def on_error(payload):
    print(f"`on_error` called in unit test!!! Something went wrong: {payload}")
