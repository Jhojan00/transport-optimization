from transport_optimization.hmath import Vector3
from transport_optimization.packages import GuillotineNode, Package


class Vehicle:
    def __init__(self, width: float, length: float, height: float):
        self.width = width
        self.length = length
        self.height = height

        self.content = GuillotineNode(
            Vector3(self.width, self.length, self.height), Vector3.zero()
        )

    def add(self, package: Package) -> GuillotineNode | None:
        inserted = self.content.insert_package(package)
        return inserted

    @property
    def volume(self) -> float:
        return self.width * self.length * self.height
