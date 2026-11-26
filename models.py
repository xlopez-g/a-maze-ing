import numpy as np
import numpy.typing as npt
from typing import Any
from enum import Enum


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


class PrintMaze(Maze):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.grid = np.full((height, width), " ", dtype=object)

        for x in range(width):
            for y in range(height):
                if y % 2 != 0 and x % 2 != 0:
                    if x < width - 1:
                        self.grid[y, x + 1] = "┃"
                    if y < height - 1:
                        self.grid[y + 1, x] = "━"
                self.grid[y, 0] = "┃"
                self.grid[0, x] = "━"
                self.grid[y, width - 1] = "┃"
                self.grid[height - 1, x] = "━"

        self.grid[0, 0] = "┏"
        self.grid[height - 1, 0] = "┗"
        self.grid[0, width - 1] = "┓"
        self.grid[height - 1, width - 1] = "┛"


class COLORS(Enum):
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    grey = "\033[90m"
    reset = "\033[0m"
    purple = "\033[35m"
    maroon = "\033[38;5;52m"
    orange = "\033[38;5;208m"
    brown = "\033[33m"
    gold = "\033[38;5;220m"
    darkred = "\033[38;5;88m"
    crimson = "\033[38;5;161m"
    cyan = "\033[36m"
    lime = "\033[92m"
    magenta = "\033[35m"
