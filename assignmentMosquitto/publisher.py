# python 3.11

import random
import time
import string

from paho.mqtt import client as mqtt_client


#define a set of random characters
letters = string.ascii_lowercase
# Set packet size to desired byte size
PACKET_SIZE = 256
TOTAL_MESSAGES = 100
test_packet = "\x00"*max(PACKET_SIZE, 0) 

def randomData(length, letters):
    return ''.join(random.choice(letters) for i in range(length))
    
def generateDataArray(PACKET_SIZE, letters):
    bodyArray = []
    body = randomData(PACKET_SIZE, letters)
    for i in range(TOTAL_MESSAGES) :
        bodyArray.append(randomData(PACKET_SIZE, letters))
    return bodyArray




broker = '192.168.123.233'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, bodyArray):
    st = time.time()
    for i, payload in enumerate(bodyArray):
        message = f"{i}:{payload}"
        result = client.publish(topic, message, 2) # 2 indicated QoS
        status = result[0]
        #if status == 0:
            #print(f"Send `{message}` to topic `{topic}`")
        if status != 0:
            print(f"Failed to send message to topic {topic}")
    et = time.time()
    elapsedTime = et - st
    print("Time taken to deliver all ", TOTAL_MESSAGES, "messages: ", elapsedTime, "seconds.")
    print("Rate: ",  TOTAL_MESSAGES / elapsedTime, "message/sec.")

    return


def run():
    bodyArray = generateDataArray(PACKET_SIZE, letters)    
    print("body array created, with size: ", len(bodyArray))
    client = connect_mqtt()
    #client.loop_start()  ## persistant loop incase of disconnect
    publish(client, bodyArray)
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':    
    run()
