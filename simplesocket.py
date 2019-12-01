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
        self.s.bind(('', port))

    def listen(self):
        self.s.listen()
        self.c, addr = self.s.accept()
        print(" Connected to: " + addr)
        self.c.send('Thank you for connecting')

    def close(self):
        self.c.close()
