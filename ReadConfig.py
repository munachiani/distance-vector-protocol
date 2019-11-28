
# config file format
# <num-servers>
# <num-neighbors>
# <server-ID> <server-IP> <server-port>
# <server-ID1> <server-ID2> <cost>
# todo class type for server, id, ip, port, costtoserver1

import TopoServer

def openFile():
    file = open("config.txt", 'r')
    return file

def printFile(f):
    print(f.read())

def getServers(f):
    s = f.readline(1)
    return str(s)
    # for i in range(0, int(s))




if __name__ == '__main__':
    config = openFile()
    print("Servers in this config: " + getServers(config))
    printFile(config)
