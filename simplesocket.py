# https://www.geeksforgeeks.org/socket-programming-python/
# used as reference for socket server.
import socket


class Simplesocket:
    def __init__(self, id, ip, port):
        self.s = socket.socket()
        self.port = port
        self.id = id
        self.ip = ip
        self.s.bind(('', port))
        self.s.listen(5)

    def listen(self):
        self.c, addr = self.s.accept()
        print(" Connected to: " + addr)
        self.c.send('Thank you for connecting')

    def close(self):
        self.c.close()
