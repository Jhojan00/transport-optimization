from transport_optimization.storage import load_graph_json

class TransportGraph:
    def __init__(self):
        self.adjacency_list: dict = load_graph_json()

    def get_graph(self) -> dict:
        return self.adjacency_list # Retorna el diccionario de adyacencia del grafo

    def reload(self) -> None:
        self.adjacency_list = load_graph_json() # Recarga el grafo desde el almacenamiento si hubo cambios