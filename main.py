from collections.abc import Callable

import flet as ft
import flet_map as ftm

from transport_optimization.graph import TransportGraph
from transport_optimization.ui_components import (
    Counter,
    Header,
    Map,
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
    map_layers: list[ftm.MapLayer],
    start_optimization: Callable,
) -> ft.Column:

    header = Header()
    start = ft.Button("Start", on_click=start_optimization)
    menu = Menu([VehiclesMenu(vehicles), PackagesMenu(packages), start])
    map = Map(map_layers)

    body = ft.Row([map, menu], expand=10)

    content = ft.Column(
        [header, body],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return content


def draw_route(markers_layer: ftm.MarkerLayer, lines_layer: ftm.PolylineLayer):
    graph = TransportGraph()

    for node in graph.adjacency_list:
        coords = graph.coordinates[node]
        draw_marker(
            markers_layer,
            ftm.MapLatitudeLongitude(coords["lat"], coords["lon"]),
            tooltip=node,
        )

    for node, conn in graph.adjacency_list.items():
        node_cords = graph.coordinates[node]
        for city in conn:
            city_cords = graph.coordinates[city["dest"]]

            draw_line(
                lines_layer,
                ftm.MapLatitudeLongitude(node_cords["lat"], node_cords["lon"]),
                ftm.MapLatitudeLongitude(city_cords["lat"], city_cords["lon"]),
            )


@ft.component
def App():

    vehicles = [
        Counter(ft.Icons.MOTORCYCLE, "Motorbike", 2, "Size: (0.5, 0.5, 0.5) m"),
        Counter(ft.Icons.LOCAL_SHIPPING, "Van", 20, "Size: (1.4, 3.2, 1.5) m"),
        Counter(ft.Icons.DIRECTIONS_TRANSIT, "Truck", 10, "Size: (2.3, 5.0, 2.0) m"),
    ]

    packages = Counter(ft.Icons.OUTBOX, "Packages", 10, "Random Generated Package")

    markers_layer = ftm.MarkerLayer([])
    lines_layer = ftm.PolylineLayer([])
    map_layers = [lines_layer, markers_layer]

    draw_route(markers_layer, lines_layer)

    def start_optimization():
        # TODO: Implement optimization.
        # optimize(vehicles, packages, markers_layer, lines_layer)
        pass

    return AppView(vehicles, packages, map_layers, start_optimization)


def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN_100)
    page.title = "Transport Optimization"

    page.render(App)


if __name__ == "__main__":
    ft.run(main)
