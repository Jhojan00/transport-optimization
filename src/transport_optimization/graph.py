from transport_optimization.storage import load_coordinates_json, load_graph_json


class TransportGraph:
    def __init__(self):
        self.adjacency_list: dict = load_graph_json()
        self.coordinates: dict = load_coordinates_json()

    def get_graph(self) -> dict:
        return (
            self.adjacency_list
        )  # Retorna el diccionario de adyacencia del grafo completo

    def reload(self) -> None:
        self.adjacency_list = load_graph_json()
        self.coordinates = load_coordinates_json()

    def get_sparse_graph(self, max_neighbors: int = 3) -> dict:
        # 1. Diccionario temporal para asegurar conexiones bidireccionales sin duplicados
        temp_graph = {node: {} for node in self.adjacency_list.keys()}

        # 2. Filtrar los K vecinos más cercanos por cada nodo
        for node, edges in self.adjacency_list.items():
            # Ordenamos la lista de conexiones de menor a mayor peso
            sorted_edges = sorted(edges, key=lambda edge: edge["weight"])

            # Tomamos solo los 'max_neighbors' más cercanos
            for edge in sorted_edges[:max_neighbors]:
                dest = edge["dest"]
                weight = edge["weight"]

                # Registramos la conexión de ida y de vuelta para evitar caminos ciegos
                temp_graph[node][dest] = weight
                temp_graph[dest][node] = weight

        # 3. Convertir de nuevo al formato original
        sparse_graph = {}
        for node, connections in temp_graph.items():
            sparse_graph[node] = [
                {"dest": d, "weight": w} for d, w in connections.items()
            ]

        return sparse_graph

