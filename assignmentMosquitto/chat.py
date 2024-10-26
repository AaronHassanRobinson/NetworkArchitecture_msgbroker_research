import paho.mqtt.client as mqtt
import random


client_id = f'publish-{random.randint(0, 1000)}'


def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic: {message.topic}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)


client.on_message = on_message

broker_address = '192.168.123.233'  # Example broker
client.connect(broker_address)

client.subscribe("python/mqtt")

client.loop_start()

try:
    # Keep the script running to listen for messages
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()