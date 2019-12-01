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


    def listen(self):
        self.s.bind(('', self.port))
        self.s.listen()
        self.c, addr = self.s.accept()
        print(" Connected to: " + str(addr) )
        msg = 'Thank you for connecting to: ' + str(addr)
        self.c.send(msg.encode())

    def close(self):
        self.c.close()


    def connect(self):
        self.s.connect((self.ip, self.port))
        print(self.s.recv(1024))
        self.s.close()
