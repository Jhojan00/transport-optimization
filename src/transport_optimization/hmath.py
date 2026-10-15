import copy
import math
from typing import Literal

Axis = Literal["x", "y", "z"]


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def copy(self) -> Vector3:
        return copy.deepcopy(self)

    def volume(self) -> float:
        return self.x * self.y * self.z

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other: Vector3) -> Vector3:
        return self.__add__(other)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rsub__(self, other: Vector3) -> Vector3:
        return Vector3(other.x - self.x, other.y - self.y, other.z - self.z)

    def __abs__(self) -> float:
        sm = self.x**2 + self.y**2 + self.z**2
        return math.sqrt(sm)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return False

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other: Vector3) -> bool:
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other: Vector3) -> bool:
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __gt__(self, other: Vector3) -> bool:
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other: Vector3) -> bool:
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    @staticmethod
    def vector_in(v: Vector3, a: Vector3, b: Vector3) -> bool:
        return a <= v <= b

    @staticmethod
    def zero() -> Vector3:
        return Vector3(0, 0, 0)
