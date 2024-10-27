from proton import Message

from proton.handlers import MessagingHandler

from proton.reactor import Container

USER = "admin"
PASSWORD = "password"
HOST = '192.168.123.233'
PORT = '5672'

host = HOST + ":" + PORT





class Consumer(MessagingHandler):

    def __init__(self, server, address):
        super(Consumer, self).__init__()
        self.server = server
        self.address = address


    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)
        #event.container.create_sender(conn, self.address)


    #def on_sendable(self, event):
        #event.sender.send(Message(body="Hello World!"))
        #event.sender.close()

        pass
    def on_message(self, event):
        print(event.message.body)
        event.connection.close()

Container(Consumer(host, "queue")).run()