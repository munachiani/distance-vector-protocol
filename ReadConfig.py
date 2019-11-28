
# config file format
# <num-servers>
# • <num-neighbors>
# • <server-ID> <server-IP> <server-port>
# • <server-ID1> <server-ID2> <cost>
# todo class type for server, id, ip, port, costtoserver1


def openFile():
    file = open("config.txt", 'r')
    return file

def printFile(f):
    print(f.read())




if __name__ == '__main__':
    config = openFile()
    printFile(config)
