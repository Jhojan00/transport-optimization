from dataclasses import dataclass

import flet as ft
import flet_map as ftm


@ft.component
def Header(name: str = "Transport Optimization") -> ft.Card:
    parent = ft.Card(
        ft.Row(
            [
                ft.Text(
                    name,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Icon(ft.Icons.TWO_WHEELER, size=40),
            ],
            ft.MainAxisAlignment.CENTER,
        ),
        elevation=3,
        expand=1,
        bgcolor=ft.Colors.GREEN_100,
    )

    return parent


@ft.component
def Map(extra_layers: list[ftm.MapLayer] | None = None) -> ft.Container:
    if extra_layers is None:
        extra_layers = []

    return ft.Container(
        expand=True,
        content=ftm.Map(
            initial_center=ftm.MapLatitudeLongitude(4.4389, -75.2322),
            initial_zoom=8,
            expand=True,
            layers=[
                ftm.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    user_agent_package_name="flet-map-transport-optimization/1.0",
                    on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                ),
                ftm.SimpleAttribution(text="OpenStreetMap contributors"),
                *extra_layers,
            ],
        ),
        border_radius=10,
    )


def draw_line(
    layer: ftm.PolylineLayer,
    a: ftm.MapLatitudeLongitude,
    b: ftm.MapLatitudeLongitude,
    color: ft.Color = ft.Colors.LIGHT_BLUE_100,
    width: float = 3,
):
    line = ftm.PolylineMarker([a, b], color=color, stroke_width=width)
    layer.polylines.append(line)


def draw_marker(
    layer: ftm.MarkerLayer,
    point: ftm.MapLatitudeLongitude,
    content: ft.Control | None = None,
):

    if content is None:
        content = ft.Container(
            bgcolor=ft.Colors.INDIGO, border_radius=10, width=10, height=10
        )

    marker = ftm.Marker(content, coordinates=point)
    layer.markers.append(marker)


@ft.observable
@dataclass
class Counter:
    icon: ft.IconData
    name: str
    amount: int
    tooltip: str = ""

    def add(self, amount: int = 1):
        self.amount += amount
        self.amount = max(0, self.amount)


@ft.component
def CounterView(counter: Counter) -> ft.Row:

    def add(amount: int = 1):
        counter.add(amount)

    return ft.Row(
        [
            ft.Icon(counter.icon),
            ft.Text(counter.name),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda _: add(-1)),
            ft.Text(str(counter.amount)),
            ft.IconButton(ft.Icons.ADD, on_click=lambda _: add()),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        tooltip=counter.tooltip,
    )


@ft.component
def VehiclesMenu(vehicles: list[Counter]) -> ft.Card:
    return ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Vehicles", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    *[CounterView(vehicle) for vehicle in vehicles],
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )


@ft.component
def PackagesMenu(package: Counter) -> ft.Card:
    return ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Packages", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    CounterView(package),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )


@ft.component
def Menu(components: list[ft.Control]) -> ft.Container:
    return ft.Container(
        ft.Column(
            components,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=300,
        padding=10,
    )
