import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result: {rc}')
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(f'Received PUBLISH: topic={msg.topic}, payload: {msg.payload}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io")

client.loop_forever()
