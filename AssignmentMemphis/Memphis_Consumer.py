from __future__ import annotations
import asyncio
from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError
import time


async def main():
    async def msg_handler(msgs, error, context):
        i = 0
        # try:
            
        st = time.time()
        for msg in msgs:
            string = msg.get_data().decode('utf-8')
            print(string)
            await msg.ack()
            i+=1
            print("i: ", i)
            if i == 10:
                et = time.time()
                elapsedTime = et - st
                print("Time taken to consume all messages: ", elapsedTime, "seconds.")
                print("Rate: ", 12 / elapsedTime, "message/sec.")
                break
            if error:
                print(error)
    
        
        # except (MemphisError, MemphisConnectError, MemphisHeaderError) as e:
        #     print(e)
        #     return
        
        

    try:
        memphis = Memphis()
        await memphis.connect(host="192.168.123.233", username="consumer", password="Password123$", account_id=1)
        consumer = await memphis.consumer(station_name="station", consumer_name="consumer", consumer_group="consumer")
        consumer.set_context({"key": "value"})
        consumer.consume(msg_handler)
        # Keep your main thread alive so the consumer will keep receiving data
        await asyncio.Event().wait()
        
    except (MemphisError, MemphisConnectError) as e:
        print(e)
        await memphis.close()
        exit(1)
        
    finally:
        await memphis.close()
        
if __name__ == "__main__":
    asyncio.run(main())