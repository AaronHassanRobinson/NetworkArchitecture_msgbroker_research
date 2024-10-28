import rabbitpy
import time
from timeit import Timer
import timeit
import random
import string

#define a set of random characters
letters = string.ascii_lowercase
# Set packet size to desired byte size
PACKET_SIZE = 2**23
TOTAL_MESSAGES = 10
test_packet = "\x00"*max(PACKET_SIZE, 0) 

def randomData(length, letters):
    return ''.join(random.choice(letters) for i in range(length))
    
def generateDataArray(PACKET_SIZE, letters):
    bodyArray = []
    body = randomData(PACKET_SIZE, letters)
    for i in range(TOTAL_MESSAGES) :
        bodyArray.append(randomData(PACKET_SIZE, letters))
    return bodyArray

    

def publish(channel, bodyArray):
    #body = test_packet
    # bodyArray = []
    # body = randomData(PACKET_SIZE, letters)
    # for i in range(TOTAL_MESSAGES) :
    #     bodyArray.append(randomData(PACKET_SIZE, letters))
    
    #message = rabbitpy.Message(channel, body, {'content_type': 'text/plain'})
    st = time.time()
    # for i in range(TOTAL_MESSAGES):
    #     delivered = message.publish('rabbitpy-tests', 'rt-key', mandatory=True)
    #     # if delivered:

    #     #     print('Message delivered')
    #     # else:
    #     #     print('Delivery failed')
    #     if not delivered:
    #         print('Delivery failed')
    for payload in bodyArray:
        message = rabbitpy.Message(channel, payload, {'content_type': 'text/plain'})
        delivered = message.publish('rabbitpy-tests', 'rt-key', mandatory=True)
        # if delivered:
        #     print('Message delivered')
        # else:
        #     print('Delivery failed')
        if not delivered:
            print('Delivery failed')
            
    et = time.time()
    elapsedTime = et - st
    print("Time taken to deliver all ", TOTAL_MESSAGES, "messages: ", elapsedTime, "seconds.")
    print("Rate: ",  TOTAL_MESSAGES / elapsedTime, "message/sec.")
    
    
    
if __name__ == '__main__':
    # I have created a new admin user "test" with password "test"
    # The below is the IP of the proxy
    url = "amqp://admin:password@192.168.123.233:5672//"
    
    #Generate data:
    bodyArray = generateDataArray(PACKET_SIZE, letters)    
    print("body array created, with size: ", len(bodyArray))
    try:
        with rabbitpy.Connection(url) as connection:
            with connection.channel() as channel:
                # enabled publisher confirms
                channel.enable_publisher_confirms()
                #t = Timer(lambda: publish(channel))
                #print("Time taken: " , t.timeit(number=1000))
                
                publish(channel, bodyArray)
    except rabbitpy.exceptions.MessageReturnedException as ex:
        print("Failed to publish")
    except KeyboardInterrupt:
        print('exiting...')