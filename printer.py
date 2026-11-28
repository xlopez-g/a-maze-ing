import numpy as np
from models import HexMaze, PrintMaze, COLORS

def print_box(matrix: np.ndarray) -> None:
    height, width = matrix.shape
    for yindex in range(height):#imprime cuadrado a cuadrado incluyendo los bordes
        for xindex in range(width):
            if matrix[yindex, xindex] == "XX":
                print(COLORS.green.value, "██",
                      COLORS.reset.value, sep ="", end="")
            elif matrix[yindex, xindex] == "EE":
                print(COLORS.red.value, "██",
                      COLORS.reset.value, sep="", end="")
            elif matrix[yindex, xindex] == "42":
                print(COLORS.magenta.value, "██",
                      COLORS.reset.value, sep="", end="")
            elif matrix[yindex, xindex] == "SS":
                print(COLORS.cyan.value, "██",
                      COLORS.reset.value, sep="", end="")
            else:
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
    for yindex in range(height):
        for xindex in range(width):
            cells = int(hex_maze[yindex, xindex], 16)
            if not cells & 2:
                #print("E", end="-")
                matrix[yindex * 2 + 1, xindex * 2 + 2] = "  "
            if not cells & 4:
                #print("S", end="-")
                matrix[yindex * 2 + 2, xindex * 2 + 1] = "  "
            if cells == 15:
                matrix[yindex * 2 + 1, xindex * 2 + 1] = "42"
            #else:
                #print("N/A", end="|")
        #print("")
            

def mark_positions(matrix: np.ndarray, entry: tuple[int, int], exit: tuple[int, int]) -> None:
    
    xentry, yentry = entry
    xexit, yexit = exit

    matrix[yentry * 2 + 1 , xentry * 2 + 1] = "XX"
    matrix[yexit * 2 + 1 , xexit * 2 + 1] = "EE"


def mark_solution(matrix: np.ndarray,
                  entry: tuple[int, int],
                  path: str) -> None:

    currentx, currenty = entry
    index = 0
    while index < len(path):
        #print(path[index])
        match path[index]:
            case "N":
                currenty -= 1
                matrix[currenty * 2 + 2, currentx *2 + 1] = "SS"
            case "E":
                currentx += 1
                matrix[currenty * 2 + 1, currentx *2 ] = "SS"
            case "S":
                currenty += 1
                matrix[currenty * 2 , currentx *2 + 1] = "SS"
            case "W":
                currentx -= 1
                matrix[currenty * 2 + 1, currentx *2 + 2] = "SS"
        matrix[currenty * 2 + 1, currentx *2 + 1] = "SS"
        index += 1
    
def printer(hex_maze: HexMaze,
            entry_point: tuple[int, int],
            exit_point: tuple[int, int],
            solution_path: str):

    simple_square = "██"

    #altura y anchura real para poder representar en la terminal junto al borde exterior
    width = hex_maze.width * 2 + 1
    height = hex_maze.height * 2 + 1

    matrix = np.full((height, width), simple_square)

    open_cells(matrix)
    open_passages(matrix, hex_maze)
    mark_solution(matrix, entry_point, solution_path)
    mark_positions(matrix, entry_point, exit_point)
    
    print_box(matrix)
    #print(solution_path)

    
