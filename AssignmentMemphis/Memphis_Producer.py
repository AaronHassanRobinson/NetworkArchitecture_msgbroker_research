from __future__ import annotations

import asyncio

from memphis import (
    Headers,
    Memphis,
    MemphisConnectError,
    MemphisError,
    MemphisHeaderError,
    MemphisSchemaError,
)
import random
import string
import time

#define a set of random characters
letters = string.ascii_lowercase
# Set packet size to desired byte size
PACKET_SIZE = 2**20
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




# Not using async funcs 
async def publish(bodyArray):
    try:
        memphis = Memphis()
        await memphis.connect(
            host="192.168.123.233",
            username="user",
            password="Password123$",
            account_id=1)

        producer = await memphis.producer(
            station_name="station", producer_name="producer"
        )
        headers = Headers()
        headers.add("key", "value")
        
        st = time.time()
        for i, payload in enumerate(bodyArray) :
            await producer.produce(
                bytearray(str(i)+":"+payload, "utf-8"),
                headers=headers,
            )  # you can send the message parameter as dict as well
        et = time.time()
        elapsedTime = et - st
        print("Time taken to deliver all ", TOTAL_MESSAGES, "messages: ", elapsedTime, "seconds.")
        print("Rate: ",  TOTAL_MESSAGES / elapsedTime, "message/sec.")

            
            

    except (
        MemphisError,
        MemphisConnectError,
        MemphisHeaderError,
        MemphisSchemaError,
    ) as e:
        print(e)

    finally:
        await memphis.close()


if __name__ == "__main__":
    bodyArray = generateDataArray(PACKET_SIZE, letters)    
    print("body array created, with size: ", len(bodyArray))
    asyncio.run(publish(bodyArray))