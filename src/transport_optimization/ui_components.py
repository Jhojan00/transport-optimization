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


@ft.observable
@dataclass
class MapLayers:
    markers_layer: ftm.MarkerLayer
    lines_layer: ftm.PolylineLayer

    def append_marker(self, marker: ftm.Marker):
        self.markers_layer = ftm.MarkerLayer([*self.markers_layer.markers, marker])

    def append_line(self, line: ftm.PolylineMarker):
        self.lines_layer = ftm.PolylineLayer([*self.lines_layer.polylines, line])

    def reset(self):
        self.markers_layer = ftm.MarkerLayer([])
        self.lines_layer = ftm.PolylineLayer([])


@ft.component
def Map(extra_layers: MapLayers) -> ft.Container:
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
                extra_layers.lines_layer,
                extra_layers.markers_layer,
            ],
        ),
        border_radius=10,
    )


def draw_line(
    map_layers: MapLayers,
    a: ftm.MapLatitudeLongitude,
    b: ftm.MapLatitudeLongitude,
    color: ft.Color = ft.Colors.LIGHT_BLUE_100,
    width: float = 2,
):
    line = ftm.PolylineMarker([a, b], color=color, stroke_width=width)
    map_layers.append_line(line)


def draw_marker(
    map_layers: MapLayers,
    point: ftm.MapLatitudeLongitude,
    content: ft.Control | None = None,
    tooltip: str | None = None,
    color: ft.Color = ft.Colors.INDIGO,
):

    if content is None:
        content = ft.Container(
            bgcolor=color,
            border_radius=10,
            width=10,
            height=10,
            tooltip=tooltip,
        )

    marker = ftm.Marker(content, coordinates=point)
    map_layers.append_marker(marker)


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


@ft.observable
@dataclass
class Locations:
    locations: list[str]
    chosen: str | None = None

    def pick(self, location: str):
        if not location in self.locations:
            return

        self.chosen = location


@ft.component
def ConfigMenu(locations: Locations):
    return ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Config", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column(
                        [
                            ft.Text("Starting point"),
                            ft.Dropdown(
                                value=locations.chosen,
                                options=[
                                    ft.DropdownOption(loc)
                                    for loc in locations.locations
                                ],
                            ),
                        ]
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )


@ft.observable
@dataclass
class Info:
    motorbikes: int
    vans: int
    trucks: int
    missing: int

    def set(self, motorbikes: int, vans: int, trucks: int, missing: int):
        self.motorbikes = max(0, motorbikes)
        self.vans = max(0, vans)
        self.trucks = max(0, trucks)

        self.missing = missing


@ft.component
def InfoMenu(info: Info):
    return ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Info", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text(f"Motorbikes: {info.motorbikes} Vans: {info.vans}"),
                    ft.Text(f"Trucks: {info.trucks} Missing: {info.missing}"),
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
