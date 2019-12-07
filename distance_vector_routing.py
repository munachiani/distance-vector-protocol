import socket
import threading
import json
import logging
import time

packet_count = 0


def bellman_ford(graph, source):
    d, p = {}, {}

    for node in graph:
        d[node] = float('inf')
        p[node] = None

    # set distance to 0 because the source is 0 distance from itself
    d[source] = 0
    # relax the edge V-1 times to find all the shortest path
    for _ in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]:
                if d[v] > d[u] + graph[u][v]:
                    d[v] = d[u] + graph[u][v]
                    p[v] = u

    return d, p


def load_topology(filename):
    addresses, graph = {}, {}
    with open(filename, 'r') as topology:
        lines = topology.readlines()
        # print(lines)
        num_of_nodes = int(lines[0])

        for node in range(num_of_nodes):
            graph.setdefault(node + 1, {})

        for line_num, line in enumerate(lines[2:]):
            if line_num < num_of_nodes:
                tokens = line.split()
                addresses[int(tokens[0])] = (tokens[1], int(tokens[2]))
            else:
                tokens = list(map(int, line.split()))
                graph[tokens[0]][tokens[1]] = tokens[2]

    return addresses, graph


def request_listener(server, graph):
    global packet_count
    while True:
        request, message = server.recvfrom(1024)[0].split('|')

        if request == 'update':
            loaded = json.loads(message)
            str_source_id = loaded.keys()[0]
            source_id = int(str_source_id)

            items = loaded[str_source_id].items()

            if len(items) == 1:
                destination_id, cost = int(items[0][0]), float(items[0][1])

                graph[source_id][destination_id] = cost
                graph[destination_id][source_id] = cost
            else:
                for destination_id, cost in items:
                    graph[source_id][int(destination_id)] = cost
        packet_count += 1


def neighbours_update(server, source, addresses, mapping):
    for address_id in addresses:
        if address_id != source:
            message = 'update|' + json.dumps(mapping)
            server.sendto(message.encode('utf-8'), addresses[address_id])


def main():

    global packet_count

    addresses = {}
    graph = {}
    running = False
    source_node = 0
    server = None

    print(f'Start Server with: server -t <topology-file> -i  <routing-update-interval>')

    while True:
        response = input('>>> ').split()

        if response:
            command = response[0].lower()

            if running:
                if command == 'disable' and len(response) == 2:
                    pass
                elif command == 'disable':
                    print('disable <server-id>')
                    continue

                if command == 'update' and len(response) == 4:
                    source_id = int(response[1])
                    destination_id = int(response[2])
                    cost = float(response[3])

                    # Update table locally
                    graph[source_id][destination_id] = cost
                    graph[destination_id][source_id] = cost

                    neighbours_update(server, source_node, addresses, {
                        source_id: {destination_id: cost}
                    })
                    print(f'\n {command} SUCCESS')
                    continue

                elif command == 'update':
                    print('update <server-id-1> <server-id-2> <cost>')
                    continue

                if command == 'crash':
                    server.close()
                    return
                # display and sort thr current table
                elif command == 'display':
                    distance_vector, hops = bellman_ford(graph, source_node)

                    for node in distance_vector:
                        if distance_vector[node] != 0:
                            next_hop = str(hops[node]) if hops[node] else 'none'
                            print(f'{node:^10} {next_hop:^10} {distance_vector[node]:^10}')
                    print(f'\n {command} SUCCESS')
                #     display the number of packets the server has received
                elif command == 'packets':
                    print(f'Packets received: {packet_count}')
                    packet_count = 0
                    print(f'\n {command} SUCCESS')
                #     update neighbours right away
                elif command == 'step':
                    neighbours_update(server, source_node, addresses, {
                        source_node: graph[source_node]
                    })
                    print(f'\n {command} SUCCESS')
                else:
                    print(f'{command} is not a valid command.')
            else:
                # load the topology
                if command == 'server' and len(response) == 5:
                    addresses, graph = load_topology(response[2])

                    for node in graph:
                        if graph[node]:
                            source_node = node
                            break
                    # Start the UDP server
                    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    server.bind(addresses[source_node])

                    listener = threading.Thread(target=request_listener, args=(server, graph), daemon=True)
                    listener.start()

                    print(f'Server running...')
                    running = True
                else:
                    print('Server is not running. Start it by typing:')
                    print('server -t <topology-file> -i  <routing-update-interval>')


if __name__ == '__main__':
    main()
