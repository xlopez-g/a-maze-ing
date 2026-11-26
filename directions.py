from models import CellMaze, Cell


def define_direction(pos_init: tuple[int, int],
                     pos_next: tuple[int, int]) -> str:

    y = pos_init[0]
    x = pos_init[1]
    next_y = pos_next[0]
    next_x = pos_next[1]

    if y - next_y == -1:
        direction = "south"
    elif y - next_y == 1:
        direction = "north"
    elif x - next_x == 1:
        direction = "west"
    elif x - next_x == -1:
        direction = "east"

    return (direction)


def short_direction(pos_init: tuple[int, int],
                    pos_next: tuple[int, int]) -> str:

    y = pos_init[0]
    x = pos_init[1]
    next_y = pos_next[0]
    next_x = pos_next[1]

    direction = ""

    if y - next_y == -1:
        direction = "S"
    elif y - next_y == 1:
        direction = "N"
    elif x - next_x == 1:
        direction = "W"
    elif x - next_x == -1:
        direction = "E"

    return (direction)


def create_conexion(cell1: Cell,
                    cell2: Cell,
                    direction: str) -> None:

    if direction == "north":
        cell1.north = 0
        cell2.south = 0

    elif direction == "east":
        cell1.east = 0
        cell2.west = 0

    elif direction == "south":
        cell1.south = 0
        cell2.north = 0

    elif direction == "west":
        cell1.west = 0
        cell2.east = 0
    else:
        return


def create_wall(cell1: Cell,
                cell2: Cell,
                direction: str) -> None:

    if direction == "north":
        cell1.north = 1
        cell2.south = 1

    elif direction == "east":
        cell1.east = 1
        cell2.west = 1

    elif direction == "south":
        cell1.south = 1
        cell2.north = 1

    elif direction == "west":
        cell1.west = 1
        cell2.east = 1
    else:
        return


def three_wall_cells(maze: CellMaze
                     ) -> list[tuple[int, int]]:

    three_wall_list = []

    height = maze.height
    width = maze.width

    for x in range(width):
        for y in range(height):
            cell = maze.grid[y, x]
            if (cell.north + cell.east + cell.south + cell.west) == 3:
                three_wall_list.append((y, x))

    print("lista d 3paredes", three_wall_list)

    return (three_wall_list)
