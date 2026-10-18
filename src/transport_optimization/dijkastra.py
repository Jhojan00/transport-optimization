import heapq


def calculate_shortest_path(graph: dict, start_node: str):
    # Inicializamos distancias en infinito
    distances = {node: float("inf") for node in graph}
    distances[start_node] = 0

    # priority_queue almacena tuplas: (distancia_acumulada, nodo)
    priority_queue = [(0, start_node)]
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Si encontramos una distancia acumulada mayor a la registrada, la descartamos
        if current_distance > distances[current_node]:
            continue

        # Iteramos sobre la lista de conexiones [{"dest": ..., "weight": ...}]
        for edge in graph.get(current_node, []):
            neighbor = edge["dest"]
            weight = edge["weight"]
            distance = current_distance + weight

            # Si encontramos un camino más corto hacia el vecino, actualizamos
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes


def get_optimal_path(
    previous_nodes: dict, start_node: str, target_node: str
) -> list[str]:
    path = []
    current_node = target_node

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes.get(current_node)

    path = path[::-1]

    if path and path[0] == start_node:
        return path
    return []


def get_route_through_waypoints(graph: dict, waypoints: list[str]) -> list[str]:
    if not waypoints or len(waypoints) < 2:
        return waypoints

    complete_path = []

    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        target = waypoints[i + 1]

        _, previous_nodes = calculate_shortest_path(graph, start)

        segment_path = get_optimal_path(previous_nodes, start, target)

        if not segment_path:
            return []

        if i == 0:
            complete_path.extend(segment_path)
        else:
            complete_path.extend(segment_path[1:])

    return complete_path

