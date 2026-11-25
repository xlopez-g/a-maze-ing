import numpy as np
from models import HexMaze, PrintMaze, COLORS

def print_box(matrix: np.ndarray) -> None:
    height, width = matrix.shape
    for yindex in range(height):#imprime cuadrado a cuadrado incluyendo los bordes
        for xindex in range(width):
            print(matrix[yindex, xindex], end="")
        print("")


def open_cells(matrix: np.ndarray) -> None:
    height, width = matrix.shape
    for yindex in range(1, height, 2):#solo los impares para localizar las celdas y no las paredes
        for xindex in range(1, width, 2):
            matrix[yindex, xindex] = "  "


def open_passages(matrix: np.ndarray, hex_maze: HexMaze) -> None:
    width = hex_maze.width
    height = hex_maze.height
    wall_height, wall_width = matrix.shape
    for yindex in range(height):
        for xindex in range(width):
            cells= int(hex_maze[yindex, xindex], 16)
            print(cells, end="")
        print("")
            

def printer(hex_maze: HexMaze,
            entry_point: tuple[int, int],
            exit_point: tuple[int, int]):

    simple_square = "██"

    #altura y anchura real para poder representar en la terminal junto al borde exterior
    width = hex_maze.width * 2 + 1
    height = hex_maze.height * 2 + 1

    matrix = np.full((height, width), simple_square)

    open_cells(matrix)
    print_box(matrix)
    open_passages(matrix, hex_maze)

    
