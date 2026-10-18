from transport_optimization.dijkastra import calculate_shortest_path, get_optimal_path
from transport_optimization.graph import TransportGraph


def probar_dijkstra():
    # Instanciamos la red vial
    net = TransportGraph()

    # Probamos usando el grafo ralo (sparse graph) con max 3 vecinos
    # para forzar rutas de múltiples saltos entre municipios
    sparse_graph = net.get_sparse_graph(max_neighbors=3)

    origen = "Ibagué"
    destino = "Honda"

    print(f"[*] Calculando ruta óptima de {origen} a {destino}...\n")

    if origen not in sparse_graph or destino not in sparse_graph:
        print(f"[!] Error: {origen} o {destino} no se encuentran en el grafo.")
        return

    distancias, prev = calculate_shortest_path(sparse_graph, origen)
    ruta = get_optimal_path(prev, origen, destino)

    if ruta:
        print(f"[✓] Ruta encontrada exitosamente:")
        print(f"    Camino: {' -> '.join(ruta)}")
        print(f"    Distancia total calculada: {distancias[destino]:.2f} km")
    else:
        print(f"[!] No existe una ruta conectada entre {origen} y {destino}.")


if __name__ == "__main__":
    probar_dijkstra()