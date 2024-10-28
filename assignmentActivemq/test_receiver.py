from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time

# Connection details
USER = "admin"
PASSWORD = "password"
HOST = '192.168.123.233'
PORT = '5672'

host = HOST + ":" + PORT

TOTAL_MESSAGES = 10 # Adjust as needed based on expected queue size


class Consumer(MessagingHandler):
    def __init__(self, server, address, total_messages):
        super(Consumer, self).__init__()
        self.server = server
        self.address = address
        self.total_messages = total_messages
        self.received = 0
        self.start_time = None
        self.end_time = None

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)
        self.start_time = time.time()  # Start timing when the receiver is created

    def on_message(self, event):
        #print(event.message.body)
        self.received += 1

        if self.received == self.total_messages:
            # End time is captured when all messages are received
            self.end_time = time.time()
            event.connection.close()
            elapsed_time = self.end_time - self.start_time
            print(f"Time taken to consume all {self.total_messages} messages: {elapsed_time:} seconds.")
            print(f"Rate: {self.total_messages / elapsed_time:} messages/second.")# Close connection to trigger on_disconnected

    def on_disconnected(self, event):
        if self.end_time is None:
            self.end_time = time.time()
        
        #elapsed_time = self.end_time - self.start_time
        #print(f"Time taken to consume all {self.total_messages} messages: {elapsed_time:.2f} seconds.")
        #print(f"Rate: {self.total_messages / elapsed_time:.2f} messages/second.")

if __name__ == '__main__':
    try:
        Container(Consumer(host, "queue", TOTAL_MESSAGES)).run()
    except KeyboardInterrupt:
        print("Exiting...")