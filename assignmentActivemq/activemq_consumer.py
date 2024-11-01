import optparse
from proton import Url
from proton.reactor import Container
from proton.handlers import MessagingHandler, TransactionHandler

USER = "admin"
PASSWORD = "password"
HOST = '192.168.123.233'
PORT = '5672'

host = HOST + ":" + PORT


class TxRecv(MessagingHandler, TransactionHandler):
    def __init__(self, url, messages, batch_size):
        super(TxRecv, self).__init__(prefetch=0, auto_accept=False)
        self.url = Url(url)
        self.expected = messages
        self.batch_size = batch_size
        self.current_batch = 0
        self.committed = 0

    def on_start(self, event):
        self.container = event.container
        self.conn = self.container.connect(self.url)
        self.receiver = self.container.create_receiver(self.conn, self.url.path)
        self.container.declare_transaction(self.conn, handler=self)
        self.transaction = None

    def on_message(self, event):
        print(event.message.body)
        self.transaction.accept(event.delivery)
        self.current_batch += 1
        if self.current_batch == self.batch_size:
            self.transaction.commit()
            self.transaction = None

    def on_transaction_declared(self, event):
        self.receiver.flow(self.batch_size)
        self.transaction = event.transaction

    def on_transaction_committed(self, event):
        self.committed += self.current_batch
        self.current_batch = 0
        if self.expected == 0 or self.committed < self.expected:
            self.container.declare_transaction(self.conn, handler=self)
        else:
            event.connection.close()

    def on_disconnected(self, event):
        self.current_batch = 0


parser = optparse.OptionParser(usage="usage: %prog [options]")
parser.add_option("-a", "--address", default=host+"/queue",
                  help="address from which messages are received (default %default)")
parser.add_option("-m", "--messages", type="int", default=100,
                  help="number of messages to receive; 0 receives indefinitely (default %default)")
parser.add_option("-b", "--batch-size", type="int", default=1,
                  help="number of messages in each transaction (default %default)")
opts, args = parser.parse_args()

try:
    Container(TxRecv(opts.address, opts.messages, opts.batch_size)).run()
except KeyboardInterrupt:
    pass