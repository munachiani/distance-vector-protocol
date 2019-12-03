

def bellman_ford(graph, source):
    d, p = {}, {}

    for node in graph:
        d[node] = float('inf')
        p[node] = None

    d[source] = 0

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
        print(num_of_nodes)

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


def main():
    addresses = {}
    graph = {}
    running = False
    source_node = 0

    print('Distance Vector Routing Protocols Emulator')

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
                    pass
                elif command == 'update':
                    print('update <server-id-1> <server-id-2> <cost>')
                    continue

                if command == 'crash':
                    return
                elif command == 'display':
                    pass
                elif command == 'packets':
                    print(0)
                elif command == 'step':
                    pass
                else:
                    print(f'{command} is not a valid command.')
            else:
                if command == 'server' and len(response) == 5:
                    addresses, graph = load_topology(response[2])

                    for node in graph:
                        if graph[node]:
                            source_node = node
                            break

                    print(f'Server is running on port {addresses[source_node][1]}, ip address is {addresses[source_node][0]}')
                    running = True
                else:
                    print('Server is not running. Start it by typing:')
                    print('server -t <topology-file> -i  <routing-update-interval>')


if __name__ == '__main__':
    main()
