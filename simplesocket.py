# https://www.geeksforgeeks.org/socket-programming-python/
# https://realpython.com/python-sockets/#multi-connection-client-and-server
#used as reference for socket server.
import socket


class Simplesocket:
    def __init__(self, id, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.id = id
        self.ip = ip

# need to update to non blocking + selectors...

    def listen(self):
        self.s.bind(('localhost', self.port))
        self.s.listen()
        self.c, addr = self.s.accept()
        msg = 'Incoming connection from: ' + str(addr)
        print(msg)
        msg = 'Connection successful! serverIP: ' + self.ip + ' yourIP: ' + str(addr)
        self.c.send(msg.encode())

    def close(self):
        print("Closing connection on: " + self.ip)
        self.c.close()


    def connect(self):
        self.s.connect((self.ip, self.port))
        print( str(self.s.recv(1024) ))
        self.s.send("Hello...".encode())
        self.s.close()
