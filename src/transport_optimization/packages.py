from transport_optimization.hmath import Axis, Vector3


class Package:
    def __init__(self, size: Vector3, start: str, end: str):
        self.size = size
        self.start = start
        self.end = end

    @property
    def volume(self):
        return self.size.volume()


class GuillotineNode:
    def __init__(self, size: Vector3, position: Vector3):
        self.size = size
        self.position = position

        self.left: GuillotineNode | None = None
        self.right: GuillotineNode | None = None

        self.cut_position: Vector3 | None = None
        self.axis: Axis | None = None

        self.package: Package | None = None

    def __cut(
        self, new_position: Vector3, axis: Axis = "x"
    ) -> tuple[GuillotineNode, GuillotineNode] | None:
        if not Vector3.vector_in(
            new_position, self.position, self.position + self.size
        ):
            return

        left_size = self.size.copy()
        right_size = self.size.copy()
        match axis:
            case "x":
                left_size.x = new_position.x - self.position.x
                right_size.x = self.size.x - left_size.x
            case "y":
                left_size.y = new_position.y - self.position.y
                right_size.y = self.size.y - left_size.y
            case "z":
                left_size.z = new_position.z - self.position.z
                right_size.z = self.size.z - left_size.z

        self.left = GuillotineNode(left_size, self.position)
        self.right = GuillotineNode(right_size, new_position)

        self.cut_position = new_position
        self.axis = axis

        return self.left, self.right

    def __best_fit(self, package: Package, candidates: list[GuillotineNode]) -> None:
        if self.left is None and self.right is None:
            fits = package.size <= self.size

            if fits:
                candidates.append(self)
                return

        if self.package is not None:
            return

        if self.left and self.left.package is None:
            self.left.__best_fit(package, candidates)

        if self.right and self.right.package is None:
            self.right.__best_fit(package, candidates)

    def insert_package(self, package: Package) -> GuillotineNode | None:
        canditates: list[GuillotineNode] = []
        self.__best_fit(package, canditates)

        target: GuillotineNode | None = None

        for candidate in canditates:
            if target is None or candidate.size.volume() < target.size.volume():
                target = candidate

        if target is None:
            return None

        new_node = target
        for axis in ("x", "y", "z"):
            cut_pos = new_node.position.copy()

            match axis:
                case "x":
                    cut_pos.x += package.size.x

                case "y":
                    cut_pos.y += package.size.y

                case "z":
                    cut_pos.z += package.size.z

            cut = new_node.__cut(cut_pos, axis)
            if cut is None:
                return
            new_node = cut[0]  # Left node.

        new_node.package = package
        return new_node

    def __get_packages(self, packages):
        if self.package is not None:
            packages.append(self.package)
            return

        if self.left is not None:
            self.left.__get_packages(packages)

        if self.right is not None:
            self.right.__get_packages(packages)

    def get_packages(self) -> list[Package]:
        packages = []
        self.__get_packages(packages)
        return packages
