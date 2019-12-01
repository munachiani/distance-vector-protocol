
# config file format
# <num-servers>
# <num-neighbors>
# <server-ID> <server-IP> <server-port>
# <server-ID1> <server-ID2> <cost>
# todo class type for server, id, ip, port, costtoserver1

import TopoServer
from simplesocket import Simplesocket

def openFile():
    file = open("config.txt", 'r')
    return file

def printFile(f):
    print(f.read())

# return config file as list of lines
def getInfo(f):
    data = f.read()
    # todo update this 8, to adapt to
    #of servers => #of lines
    lines = data.split("\n", 8)
    return lines

# how many server
def getServers(f):
    s = f.readline(1)
    return str(s)
    # for i in range(0, int(s))

# get server id = i
def getServer(d, i):
    line = d[2+i]
    # print(line)
    bits = line.split(' ')
    # print(bits)
    ip = bits[1]
    port = bits[2]
    return ip, port

def getUserInput():
    return input("Enter a command: ")


if __name__ == '__main__':
    config = openFile()
    data = getInfo(config)
    ip, port = getServer(data, 1)
    # figure out the listen loop/callbacks...
    con = Simplesocket(1, ip, int(port) )
    # con.connect()       #client side
    con.listen()      #server side
    while getUserInput().equals(0):     pass

    con.close()
