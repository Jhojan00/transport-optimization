import random
from collections.abc import Callable

import flet as ft
import flet_map as ftm

from transport_optimization.distribution import (
    distribute_packages,
    generate_packages,
    get_vehicles,
    optimal_path_vehicle,
)
from transport_optimization.graph import TransportGraph
from transport_optimization.ui_components import (
    ConfigMenu,
    Counter,
    Header,
    Info,
    InfoMenu,
    Locations,
    Map,
    MapLayers,
    Menu,
    PackagesMenu,
    VehiclesMenu,
    draw_line,
    draw_marker,
)


@ft.component
def AppView(
    vehicles: list[Counter],
    packages: Counter,
    locations: Locations,
    map_layers: MapLayers,
    info: Info,
    start_optimization: Callable,
) -> ft.Column:

    header = Header()
    start = ft.Button("Start", on_click=start_optimization)
    menu = Menu(
        [
            VehiclesMenu(vehicles),
            PackagesMenu(packages),
            ConfigMenu(locations),
            InfoMenu(info),
            start,
        ]
    )
    map = Map(map_layers)

    body = ft.Row([map, menu], expand=10)

    content = ft.Column(
        [header, body],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return content


def draw_route(
    map_layers: MapLayers,
    graph: TransportGraph,
):

    for node in graph.adjacency_list:
        coords = graph.coordinates[node]
        draw_marker(
            map_layers,
            ftm.MapLatitudeLongitude(coords["lat"], coords["lon"]),
            tooltip=node,
        )

    for node, conn in graph.adjacency_list.items():
        node_cords = graph.coordinates[node]
        for city in conn:
            city_cords = graph.coordinates[city["dest"]]

            draw_line(
                map_layers,
                ftm.MapLatitudeLongitude(node_cords["lat"], node_cords["lon"]),
                ftm.MapLatitudeLongitude(city_cords["lat"], city_cords["lon"]),
            )


def optimize(
    vehicles_amount: tuple[int, int, int],
    packages_amount: int,
    locations: Locations,
    graph: TransportGraph,
    map_layers: MapLayers,
    info: Info,
):

    vehicles = get_vehicles(*vehicles_amount)
    packages = generate_packages(packages_amount, locations.chosen, locations.locations)
    distributed, missing = distribute_packages(packages, *vehicles)

    motorbikes = 0
    vans = 0
    trucks = 0

    for vehicle in distributed:
        if vehicle.car_type == "Motorbike":
            motorbikes += 1

        elif vehicle.car_type == "Van":
            vans += 1

        else:
            trucks += 1

        path = optimal_path_vehicle(vehicle, graph.adjacency_list)
        print(path)
        path_color = ft.CupertinoColors.random()

        for i in range(len(path) - 1):
            coord_a = graph.coordinates[path[i]]
            coord_b = graph.coordinates[path[i + 1]]

            draw_line(
                map_layers,
                ftm.MapLatitudeLongitude(coord_a["lat"], coord_a["lon"]),
                ftm.MapLatitudeLongitude(coord_b["lat"], coord_b["lon"]),
                path_color,
                3,
            )

    info.set(motorbikes, vans, trucks, missing)

    coords = graph.coordinates

    draw_marker(
        map_layers,
        ftm.MapLatitudeLongitude(
            coords[locations.chosen]["lat"], coords[locations.chosen]["lon"]
        ),
        color=ft.Colors.GREEN,
    )


@ft.component
def App():

    vehicles = [
        Counter(ft.Icons.MOTORCYCLE, "Motorbike", 2, "Size: (0.5, 0.5, 0.5) m"),
        Counter(ft.Icons.LOCAL_SHIPPING, "Van", 20, "Size: (1.4, 3.2, 1.5) m"),
        Counter(ft.Icons.DIRECTIONS_TRANSIT, "Truck", 10, "Size: (2.3, 5.0, 2.0) m"),
    ]

    packages = Counter(ft.Icons.OUTBOX, "Packages", 10, "Random Generated Package")
    graph = TransportGraph()
    locations = Locations(list(map(str, graph.adjacency_list.keys())))
    locations.pick("Ibagué")
    info = Info(-1, -1, -1, -1)

    markers_layer = ftm.MarkerLayer([])
    lines_layer = ftm.PolylineLayer([])
    map_layers = MapLayers(markers_layer, lines_layer)

    draw_route(map_layers, graph)

    def start_optimization():
        map_layers.reset()
        draw_route(map_layers, graph)
        optimize(
            (vehicles[0].amount, vehicles[1].amount, vehicles[2].amount),
            packages.amount,
            locations,
            graph,
            map_layers,
            info,
        )

    return AppView(vehicles, packages, locations, map_layers, info, start_optimization)


def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN_100)
    page.title = "Transport Optimization"

    page.render(App)


if __name__ == "__main__":
    ft.run(main)
