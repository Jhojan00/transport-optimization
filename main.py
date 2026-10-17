from dataclasses import dataclass

import flet as ft
import flet_map as ftm


@ft.component
def Header() -> ft.Card:
    parent = ft.Card(
        ft.Row(
            [
                ft.Text(
                    "Transport Optimization",
                    font_family="Consolas",
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
def Map() -> ft.Container:
    return ft.Container(
        expand=True,
        content=ftm.Map(
            initial_center=ftm.MapLatitudeLongitude(4.4389, -75.2322),
            initial_zoom=7,
            expand=True,
            layers=[
                ftm.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    user_agent_package_name="flet-map-examples/1.0",
                    on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                ),
                ftm.SimpleAttribution(text="OpenStreetMap contributors"),
            ],
        ),
        border_radius=10,
    )


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
def PackagesMenu(amount: int) -> ft.Card:
    package = Counter(ft.Icons.OUTBOX, "Packages", amount, "Random Generated Package")
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


@ft.component
def App() -> ft.Column:

    vehicles = [
        Counter(ft.Icons.MOTORCYCLE, "Motorbike", 2, "Size: (0.5, 0.5, 0.5) m"),
        Counter(ft.Icons.LOCAL_SHIPPING, "Van", 20, "Size: (1.4, 3.2, 1.5) m"),
        Counter(ft.Icons.DIRECTIONS_TRANSIT, "Truck", 10, "Size: (2.3, 5.0, 2.0) m"),
    ]

    header = Header()

    menu_left = Menu([VehiclesMenu(vehicles), PackagesMenu(10)])
    menu_right = Menu([ft.Column()])

    body = ft.Row([menu_left, Map(), menu_right], expand=10)

    return ft.Column(
        [header, body],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.title = "Transport Optimization"

    page.render(App)


if __name__ == "__main__":
    ft.run(main)
