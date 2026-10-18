import itertools
from transport_optimization.api import get_tolima_cities, get_city_coordinates, fetch_osrm_distance
from transport_optimization.storage import save_graph_json
from transport_optimization.graph import TransportGraph

def main():
    print("RED VIAL TOLIMA ===")
    
    # 1. Obtener municipios crudos
    cities_data = get_tolima_cities()
    print(f"[+] Total de municipios crudos en API-Colombia: {len(cities_data)}")
    
    # 2. Obtener Coordenadas
    muni_dict = {}
    print("\n[*] Obteniendo coordenadas automáticas...")
    for city in cities_data:
        name = city.get("name")
        if name:
            coords = get_city_coordinates(name)
            if coords:
                muni_dict[name] = {"lon": coords[0], "lat": coords[1]}
                print(f"  [✓] Coordenadas de {name} obtenidas.")
            else:
                print(f"  [x] FALLÓ: No se hallaron coordenadas para {name}.")

    print(f"\n[+] Total de municipios con coordenadas válidas: {len(muni_dict)}")
    
    # 3. Inicializar Grafo
    graph_data = {muni: [] for muni in muni_dict.keys()}
    
    # 4. Todos contra Todos (Combinaciones)
    municipality_names = list(muni_dict.keys())
    # Genera combinaciones únicas (A, B) sin repetir (B, A)
    pairs = list(itertools.combinations(municipality_names, 2))
    
    print(f"\n[*] Consultando OSRM para {len(pairs)} rutas posibles...")
    print("    (Esto tomará unos ~3 a 4 minutos. Ve por un café ☕)")
    
    for origin, target in pairs:
        lon1, lat1 = muni_dict[origin]["lon"], muni_dict[origin]["lat"]
        lon2, lat2 = muni_dict[target]["lon"], muni_dict[target]["lat"]
        
        distance = fetch_osrm_distance(lon1, lat1, lon2, lat2)
        
        if distance is not None:
            # Al ser combinaciones únicas, lo inyectamos bidireccionalmente
            graph_data[origin].append({"dest": target, "weight": distance})
            graph_data[target].append({"dest": origin, "weight": distance})
            print(f"    -> [OK] {origin} <-> {target} ({distance} km)")
        else:
            print(f"    -> [FALLO] No se pudo trazar ruta entre {origin} y {target}")

    # 5. Persistencia
    print("\n[*] Guardando y validando grafo completo en memoria...")
    save_graph_json(graph_data)
    
    transport_net = TransportGraph()
    my_pure_dict_graph = transport_net.get_graph()
    
    print("\nÉXITO] GRAFO MULTIDIRECCIONAL MONTADO")
    print("Ejemplo de conexiones para Líbano:")
    print(my_pure_dict_graph.get("Líbano", [])[:5], "... (continúa)")

if __name__ == "__main__":
    main()