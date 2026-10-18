from typing import Literal

from transport_optimization.hmath import Vector3
from transport_optimization.packages import GuillotineNode, Package

CarType = Literal["Motorbike", "Van", "Truck"]


class Vehicle:
    def __init__(self, width: float, length: float, height: float, car_type: CarType):
        self.width = width
        self.length = length
        self.height = height
        self.car_type = car_type

        self.content = GuillotineNode(
            Vector3(self.width, self.length, self.height), Vector3.zero()
        )

    def add(self, package: Package) -> GuillotineNode | None:
        inserted = self.content.insert_package(package)
        return inserted

    @property
    def volume(self) -> float:
        return self.width * self.length * self.height

    @property
    def packages(self) -> list[Package]:
        return self.content.get_packages()
