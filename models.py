import numpy as np
import numpy.typing as npt
from typing import Any


class Cell:
    def __init__(self) -> None:
        self.north = 1
        self.east = 1
        self.south = 1
        self.west = 1


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.grid: npt.NDArray[np.object_] = np.empty((height, width),
                                                      dtype=object)

    def __getitem__(self, position: Any) -> Any:
        return self.grid[position]

    def __setitem__(self, position: Any, value: Any) -> None:
        self.grid[position] = value

    def __iter__(self) -> Any:
        return iter(self.grid)


class CellMaze(Maze):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        for y in range(height):
            for x in range(width):
                self.grid[y, x] = Cell()


class VisitedMaze(Maze):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.grid = np.empty((height, width), dtype=object)

        for x in range(width):
            for y in range(height):
                self.grid[y, x] = False


class BitMaze(Maze):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.grid = np.zeros((height, width), dtype=int)


class HexMaze(Maze):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.grid = np.empty((height, width), dtype=object)

        for x in range(width):
            for y in range(height):
                self.grid[y, x] = 0
