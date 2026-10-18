import itertools
from collections import deque

from transport_optimization.api import (
    fetch_osrm_route,
    get_city_coordinates,
    get_tolima_cities,
    passes_through_other_city,
)
from transport_optimization.graph import TransportGraph
from transport_optimization.storage import save_coordinates_json, save_graph_json

THRESHOLD_KM = 4.0


def connected_components(graph_data: dict) -> list[set]:
    visited, components = set(), []
    for start in graph_data:
        if start in visited:
            continue
        comp, queue = set(), deque([start])
        while queue:
            node = queue.popleft()
            if node in comp:
                continue
            comp.add(node)
            queue.extend(e["dest"] for e in graph_data[node] if e["dest"] not in comp)
        visited |= comp
        components.append(comp)
    return components


def main():
    print("=== RED VIAL TOLIMA ===")

    # 1. Municipios crudos
    cities_data = get_tolima_cities()
    print(f"[+] Total de municipios crudos en API-Colombia: {len(cities_data)}")

    # 2. Coordenadas
    muni_dict = {}
    print("\n[*] Obteniendo coordenadas automáticas...")
    for city in cities_data:
        name = city.get("name")
        if not name:
            continue
        coords = get_city_coordinates(name)
        if coords:
            muni_dict[name] = {"lon": coords[0], "lat": coords[1]}
            print(f"  [✓] Coordenadas de {name} obtenidas.")
        else:
            print(f"  [x] FALLÓ: No se hallaron coordenadas para {name}.")

    print(f"\n[+] Total de municipios con coordenadas válidas: {len(muni_dict)}")

    # 3. Guardar coordenadas.
    save_coordinates_json(muni_dict)

    # 4. Grafo: solo conexiones directas por carretera
    graph_data = {muni: [] for muni in muni_dict}
    pairs = list(itertools.combinations(muni_dict.keys(), 2))

    print(f"\n[*] Consultando OSRM para {len(pairs)} rutas posibles...")
    print("    (Esto tomará varios minutos. Ve por un café ☕)")

    ok = skipped = failed = 0
    for origin, target in pairs:
        o, t = muni_dict[origin], muni_dict[target]
        result = fetch_osrm_route(o["lon"], o["lat"], t["lon"], t["lat"])

        if result is None:
            failed += 1
            print(f"    -> [FALLO] No se pudo trazar ruta entre {origin} y {target}")
            continue

        distance, route_coords = result
        via = passes_through_other_city(
            route_coords, muni_dict, origin, target, threshold_km=THRESHOLD_KM
        )

        if via:
            skipped += 1
            print(f"    -> [SKIP] {origin} - {target} pasa por {via}")
            continue

        graph_data[origin].append({"dest": target, "weight": distance})
        graph_data[target].append({"dest": origin, "weight": distance})
        ok += 1
        print(f"    -> [OK] {origin} <-> {target} ({distance} km)")

    print(
        f"\n[+] Aristas directas: {ok} | Descartadas (indirectas): {skipped} | Fallos: {failed}"
    )

    # 5. Verificar conectividad
    components = connected_components(graph_data)
    if len(components) == 1:
        print("[✓] El grafo es conexo.")
    else:
        print(f"[!] El grafo tiene {len(components)} componentes desconectadas:")
        for comp in sorted(components, key=len):
            if len(comp) <= 5:
                print(f"    - {sorted(comp)}")
        print("    Sube THRESHOLD_KM o revisa las coordenadas de los nodos aislados.")

    # 6. Persistencia
    print("\n[*] Guardando grafo...")
    save_graph_json(graph_data)

    transport_net = TransportGraph()
    my_pure_dict_graph = transport_net.get_graph()

    print("\n[ÉXITO] GRAFO DE CONEXIONES DIRECTAS MONTADO")
    print("Ejemplo de conexiones para Líbano:")
    print(my_pure_dict_graph.get("Líbano", [])[:5], "... (continúa)")


if __name__ == "__main__":
    main()
