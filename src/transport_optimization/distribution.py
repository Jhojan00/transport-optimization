import random

from transport_optimization.hmath import Vector3
from transport_optimization.packages import Package
from transport_optimization.vehicles import Vehicle

MOTORBIKE_SIZE = (0.5, 0.5, 0.5)
VAN_SIZE = (1.4, 3.2, 1.5)
TRUCK_SIZE = (2.3, 5.0, 2.0)


def generate_packages(amount: int, start: str, destines: list[str]) -> list[Package]:
    packages = []

    for _ in range(amount):
        x = random.uniform(0.1, 1.1)
        y = random.uniform(0.1, 2.5)
        z = random.uniform(0.1, 1.0)

        package = Package(Vector3(x, y, z), start, random.choice(destines))
        packages.append(package)

    return packages


def get_vehicles(
    motorbikes: int, vans: int, trucks: int
) -> tuple[list[Vehicle], list[Vehicle], list[Vehicle]]:
    motorbikes_l = [Vehicle(*MOTORBIKE_SIZE, "Motorbike") for _ in range(motorbikes)]
    vans_l = [Vehicle(*VAN_SIZE, "Van") for _ in range(vans)]
    trucks_l = [Vehicle(*TRUCK_SIZE, "Truck") for _ in range(trucks)]

    return (motorbikes_l, vans_l, trucks_l)


def distribute_packages(
    packages: list[Package],
    motorbikes: list[Vehicle],
    vans: list[Vehicle],
    trucks: list[Vehicle],
) -> tuple[list[Vehicle], int]:
    if len(packages) <= 0:
        return [], 0

    sorted_packates: list[Package] = sorted(
        packages, key=lambda e: e.volume, reverse=True
    )
    used_vehicles: list[Vehicle] = []
    packet = 0

    for package in sorted_packates:
        done = False
        for used in used_vehicles:
            inserted = used.add(package)

            if inserted is not None:
                done = True
                packet += 1
                break

        if done:
            continue

        for vehicles in (motorbikes, vans, trucks):
            if not vehicles:
                continue

            next_v = vehicles[-1]

            if next_v.volume < package.volume:
                continue

            inserted = next_v.add(package)

            if inserted is None:
                continue

            next_v = vehicles.pop()
            used_vehicles.append(next_v)
            packet += 1
            break

    return used_vehicles, len(sorted_packates) - packet
