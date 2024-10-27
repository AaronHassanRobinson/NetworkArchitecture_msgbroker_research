import optparse
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time
import string
import random

# Connection details
USER = "admin"
PASSWORD = "password"
HOST = '192.168.123.233'
PORT = '5672'

host = HOST + ":" + PORT
hostQueue = host + "/queue"

# Message payload details
PACKET_SIZE = 256
TOTAL_MESSAGES = 1000
letters = string.ascii_lowercase

def randomData(length, letters):
    return ''.join(random.choice(letters) for i in range(length))

def generateDataArray(PACKET_SIZE, letters):
    return [randomData(PACKET_SIZE, letters) for _ in range(TOTAL_MESSAGES)]

class Producer(MessagingHandler):
    def __init__(self, url, messages, bodyArray):
        super(Producer, self).__init__()
        self.url = url
        self.confirmed = 0
        self.sent = 0
        self.total = messages
        self.bodyArray = bodyArray
        self.start_time = None

    def on_start(self, event):
        event.container.create_sender(self.url)
        self.start_time = time.time()  # Start timing when the sender is created

    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            msg = Message(id=(self.sent + 1), body=self.bodyArray[self.sent])
            event.sender.send(msg)
            self.sent += 1

    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            print(f"Time taken to deliver all {self.total} messages: {elapsed_time} seconds.")
            print(f"Rate: {self.total / elapsed_time} messages/sec.")
            event.connection.close()

    def on_disconnected(self, event):
        self.sent = self.confirmed

# Parse options
parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")

parser.add_option("-a", "--address", default=hostQueue,
                  help="address to which messages are sent (default %default)")

parser.add_option("-m", "--messages", type="int", default=TOTAL_MESSAGES,
                  help="number of messages to send (default %default)")

opts, args = parser.parse_args()

if __name__ == '__main__':
    bodyArray = generateDataArray(PACKET_SIZE, letters)
    print(f"Body array created, with size: {len(bodyArray)}")
    try:
        Container(Producer(opts.address, opts.messages, bodyArray)).run()
    except KeyboardInterrupt:
        print("Exiting...")