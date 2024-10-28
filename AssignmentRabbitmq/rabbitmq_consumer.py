import rabbitpy
import time
if __name__ == '__main__':
    
    url = "amqp://user:password@192.168.123.233:5672//"
    try:
        with rabbitpy.Connection(url) as connection:
            with connection.channel() as channel:
                queue = rabbitpy.Queue(channel, 'bigdawgs')
                print("successfully made queue")
                
                TOTAL_MESSAGES = len(queue)
                print("Total messages in queue: ", TOTAL_MESSAGES)
                
                st = time.time()
                while len(queue) > 0:
                    message = queue.get()
                    #message.pprint(True)
                    #print(str(message.body))
                    message.ack()
                    #print('There are {} more messages in the queue'.format(len(queue)))
                # try:
                et = time.time()
                elapsedTime = et - st
                print("Time taken to consume all messages: ", elapsedTime, "seconds.")
                print("rate: ", TOTAL_MESSAGES / elapsedTime, "messages/second.")

                #     for message in queue:
                #         message.pprint(True)
                #         message.ack()
                # except KeyboardInterrupt:
                #     print('exiting...')


    except rabbitpy.exceptions.MessageReturnedException as ex:
        print("Failed to consume")




    