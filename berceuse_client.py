import socket
import threading
import sys

host = ''
port = 50000
# address = ('localhost', 6005)


class Client(threading.Thread):
    def __init__(self, conn):
        super(Client, self).__init__()
        self.conn = conn
        self.data = b''

    def run(self):
        while True:
            self.data = self.data + self.conn.recv(1024)
            if self.data.endswith(b'\r\n'):

                print(self.data)

                try:
                    output = self.data.decode('utf-8')
                    print("Output / UTF8: " + output)
                except UnicodeDecodeError:
                    print("UTF-8 codec cannot decode...")

                try:
                    output = self.data.decode('ascii')
                    print("Output / ASCII: " + output)

                    if output.startswith("GO"):
                        print("===> ACTION A LANCER")

                except UnicodeDecodeError:
                    print("ASCII codec cannot decode...")

                print("--- fin du flux reçu ---")

                self.data = b''

    def send_msg(self, msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()


class ConnectionThread(threading.Thread):
    def __init__(self, host, port):
        super(ConnectionThread, self).__init__()
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((host,port))
            # self.s.bind(address)
            self.s.listen(5)
        except socket.error:
            print('Failed to create socket')
            sys.exit()
        self.clients = []

    def run(self):
        while True:
            conn, address = self.s.accept()
            message = u"\r\n"
            c = Client(conn)
            c.start()
            c.send_msg(message.encode('utf-8'))
            self.clients.append(c)
            print('[+] Client connected: {0}'.format(address[0]))

get_conns = ConnectionThread(host, port)
get_conns.start()
while True:
    try:
        response = input()
        for c in get_conns.clients:
            c.send_msg(response + u"\r\n")
    except KeyboardInterrupt:
        sys.exit()