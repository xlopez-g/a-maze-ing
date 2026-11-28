from models import CellMaze


def check_valid_neighbours(maze: CellMaze,
                           position: tuple[int, int]
                           ) -> list[tuple[int, int]]:

    height = maze.height
    width = maze.width

    y, x = position

    neighbour_list = []

    if x > 0:
        neighbour1 = (y, x - 1)
        neighbour_list.append(neighbour1)

    if x < width - 1:
        neighbour2 = (y, x + 1)
        neighbour_list.append(neighbour2)

    if y > 0:
        neighbour3 = (y - 1, x)
        neighbour_list.append(neighbour3)

    if y < height - 1:
        neighbour4 = (y + 1, x)
        neighbour_list.append(neighbour4)

    return neighbour_list


def openable_neighbours(maze: CellMaze,
                        position: tuple[int, int],
                        fourty_two_list: list[tuple[int, int]]
                        ) -> list[tuple[int, int]]:

    height = maze.height
    width = maze.width

    x = position[1]
    y = position[0]

    neighbour_list = []
    neighbour1 = y, x - 1
    neighbour2 = y, x + 1
    neighbour3 = y - 1, x
    neighbour4 = y + 1, x

    if (x > 0 and maze[y, x].east == 1
            and neighbour1 not in fourty_two_list):
        neighbour_list.append(neighbour1)

    if (x < width - 1 and maze[y, x].west == 1
            and neighbour2 not in fourty_two_list):
        neighbour_list.append(neighbour2)

    if (y > 0 and maze[y, x].north == 1
            and neighbour3 not in fourty_two_list):
        neighbour_list.append(neighbour3)

    if (y < height - 1 and maze[y, x].south == 1
            and neighbour4 not in fourty_two_list):
        neighbour_list.append(neighbour4)

    return neighbour_list


def check_open_neighbours(maze: CellMaze,
                          y: int,
                          x: int) -> list[tuple[int, int]]:

    neighbour_list = []

    if maze[y, x].north == 0:
        neighbour_list.append((y - 1, x))
    if maze[y, x].south == 0:
        neighbour_list.append((y + 1, x))
    if maze[y, x].east == 0:
        neighbour_list.append((y, x + 1))
    if maze[y, x].west == 0:
        neighbour_list.append((y, x - 1))
    return neighbour_list
