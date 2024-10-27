import optparse
from proton import Message

from proton.handlers import MessagingHandler

from proton.reactor import Container

USER = "admin"
PASSWORD = "password"
HOST = '192.168.123.233'
PORT = '5672'

host = HOST + ":" + PORT
hostQueue = host + "/queue"




class Producer(MessagingHandler):

    def __init__(self, url, messages):
        super(Producer, self).__init__()
        # self.server = server
        # self.address = address
        self.url = url
        self.confirmed = 0
        self.sent = 0
        self.total = messages

    def on_start(self, event):
        #conn = event.container.connect(self.server)
        #event.container.create_receiver(conn, self.address)
        event.container.create_sender(self.url)


    def on_sendable(self, event):
        event.sender.send(Message(body="Hello World!"))
        self.sent += 1
        event.sender.close()
        
        
    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            print("all messages confirmed")
            event.connection.close()
    
    def on_disconnected(self, event):
        self.sent = self.confirmed


    # def on_message(self, event):
    #     print(event.message.body)
    #     event.connection.close()
    
parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")

parser.add_option("-a", "--address", default=hostQueue,
                  help="address to which messages are sent (default %default)")

parser.add_option("-m", "--messages", type="int", default=1,
                  help="number of messages to send (default %default)")

opts, args = parser.parse_args()


if __name__ == '__main__':
    try:
        Container(Producer(opts.address, opts.messages)).run()
    except KeyboardInterrupt:
        pass