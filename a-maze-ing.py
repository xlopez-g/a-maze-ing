import random

import sys

from parser import parser, reader

from models import CellMaze, VisitedMaze, BitMaze, HexMaze, Cell


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


def calculate_hex(cell: Cell) -> str:

    result = (cell.north * 1
              + cell.east * 2
              + cell.south * 4
              + cell.west * 8
              )
    return format(result, "X")


def create_hex_maze(maze: CellMaze,
                    width: int,
                    height: int
                    ) -> HexMaze:

    hex_maze = HexMaze(width, height)

    for x in range(width):
        for y in range(height):
            hex_maze.grid[y, x] = calculate_hex(maze.grid[y, x])

    return hex_maze


def create_bit_maze(maze: CellMaze,
                    width: int,
                    height: int
                    ) -> BitMaze:

    bit_maze = BitMaze(width, height)

    for x in range(width):
        for y in range(height):
            bit_maze.grid[y, x] = (maze[y, x].north * 1
                                   + maze[y, x].east * 10
                                   + maze[y, x].south * 100
                                   + maze[y, x].west * 1000
                                   )

    return bit_maze


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


def reading_the_dict(parents_dict: dict[tuple[int, int], tuple[int, int]],
                     end_position: tuple[int, int]
                     ) -> str:

    path = [end_position]

    step = end_position

    while step != (0, 0):
        parent = parents_dict[step]
    #    print(temp)
        path.append(parent)
        step = parent

    # print("path:", path)
    # print("len(path)", len(path))

    result = ""

    for position_number in range((len(path)) - 1):
        initial_position = path[len(path) - position_number - 1]
        next_position = path[len(path) - position_number - 2]
        direction = short_direction(initial_position, next_position)
        result += direction

    return result


def finding_the_way(maze: CellMaze,
                    init: tuple[int, int],
                    end: tuple[int, int]
                    ) -> str:

    height = maze.height
    width = maze.width

    visited_maze = VisitedMaze(width, height)

    qeue = [init]
    parents_dict: dict[tuple[int, int], tuple[int, int]] = {}

    while (qeue):
        visited_maze.grid[qeue[0]] = True

        valid_neighbours = check_open_neighbours(maze, qeue[0][0], qeue[0][1])
        not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                  if visited_maze.grid[neighbours] is False]

        for neighbour in not_visited_neighbours:
            parents_dict.update({neighbour: qeue[0]})

        if end in not_visited_neighbours:
            break

        qeue.pop(0)
        for member in not_visited_neighbours:
            qeue.append(member)
            visited_maze.grid[member] = True

    final_path = reading_the_dict(parents_dict, end)

    return (final_path)


def create_42(maze: CellMaze
              ) -> list[tuple[int, int]]:

    height = maze.height
    width = maze.width

    if height < 7:
        print("Height not enough for 42 picture")
        fourty_two_list: list[tuple[int, int]] = []

    elif width < 9:
        print("Width not enough for 42 picture")
        fourty_two_list = []

    else:

        x = width // 2
        y = height // 2

        fourty_two_list = [(y - 2, x - 3), (y - 1, x - 3), (y, x - 3),
                           (y, x - 2), (y, x - 1),
                           (y + 1, x - 1), (y + 2, x - 1),
                           (y - 2, x + 1), (y - 2, x + 2),
                           (y - 2, x + 3), (y - 1, x + 3), (y, x + 3),
                           (y, x + 2), (y, x + 1), (y + 1, x + 1),
                           (y + 2, x + 1), (y + 2, x + 2),
                           (y + 2, x + 3)
                           ]

    return fourty_two_list


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


def open_corners(maze: CellMaze) -> None:

    height = maze.height
    width = maze.width

    if maze.grid[0, 0].south != 0:
        create_conexion(maze.grid[0, 0], maze.grid[1, 0], "south")

    if maze.grid[0, 0].west != 0:
        create_conexion(maze.grid[0, 0], maze.grid[0, 1], "east")

    if maze.grid[height - 1, 0].north != 0:
        cell = maze.grid[height - 1, 0]
        cell_next = maze.grid[height - 2, 0]
        create_conexion(cell, cell_next, "north")

    if maze.grid[height - 1, 0].west != 0:
        cell = maze.grid[height - 1, 0]
        cell_next = maze.grid[height - 1, 1]
        create_conexion(cell, cell_next, "east")

    if maze.grid[0, width - 1].south != 0:
        cell = maze.grid[0, width - 1]
        cell_next = maze.grid[1, width - 1]
        create_conexion(cell, cell_next, "south")

    if maze.grid[0, width - 1].east != 0:
        cell = maze.grid[0, width - 1]
        cell_next = maze.grid[0, width - 2]
        create_conexion(cell, cell_next, "west")

    if maze.grid[height - 1, width - 1].north != 0:
        create_conexion(maze.grid[height - 2, width - 1],
                        maze.grid[height - 1, width - 1], "south")

    if maze.grid[height - 1, width - 1].east != 0:
        create_conexion(maze.grid[height - 1, width - 1],
                        maze.grid[height - 1, width - 2], "west")


def check_zero_around(maze: CellMaze,
                      position: tuple[int, int]
                      ) -> bool:

    y = position[0]
    x = position[1]

    result = True

    if maze.grid[y - 1, x - 1].south != 0 or maze.grid[y - 1, x - 1].east != 0:
        return (False)

    if maze.grid[y + 1, x - 1].north != 0 or maze.grid[y + 1, x - 1].east != 0:
        return (False)

    if maze.grid[y - 1, x + 1].south != 0 or maze.grid[y - 1, x + 1].west != 0:
        return (False)

    if maze.grid[y + 1, x + 1].north != 0 or maze.grid[y + 1, x + 1].west != 0:
        return (False)

    return (result)


def check_threexthree_area(maze: CellMaze) -> bool:

    result = False
    height = maze.height
    width = maze.width

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            cell = maze.grid[y, x]
            cell_sum = cell.north + cell.east + cell.south + cell.west
            if cell_sum == 0:
                if check_zero_around(maze, (y, x)):
                    return True

    return (result)


def perfect_maze_solution(maze: CellMaze,
                          initial_x: int,
                          initial_y: int,
                          fourty_two_list: list[tuple[int, int]]
                          ) -> CellMaze:

    height = maze.height
    width = maze.width

    visited_maze = VisitedMaze(width, height)
    visited_list = [(initial_y, initial_x)]

    visited_maze.grid[initial_y, initial_x] = True

    for y_coord, xcoord in fourty_two_list:
        visited_maze.grid[y_coord, xcoord] = True

    while visited_list:

        y = visited_list[-1][0]
        x = visited_list[-1][1]

        valid_neighbours = check_valid_neighbours(maze, (y, x))

        not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                  if visited_maze.grid[neighbours] is False]

        if not_visited_neighbours:

            next_cell = random.choice(not_visited_neighbours)
            visited_list.append(next_cell)

            next_x = next_cell[1]
            next_y = next_cell[0]

            direction = define_direction((y, x), (next_y, next_x))

            cell = maze.grid[y, x]
            cell_next = maze.grid[next_y, next_x]
            create_conexion(cell, cell_next, direction)
            visited_maze.grid[next_cell[0], next_cell[1]] = True

        else:

            visited_list.pop()

    return (maze)


def not_perfect_maze_solution(maze: CellMaze,
                              fourty_two_list: list[tuple[int, int]]
                              ) -> CellMaze:

    height = maze.height
    width = maze.width

    open_corners(maze)

    three_wall_list = three_wall_cells(maze)
    center_x: int = width // 2
    center_y: int = height // 2

    if fourty_two_list != []:
        three_wall_list.remove((center_y - 1, center_x + 2))
        three_wall_list.remove((center_y + 1, center_x + 2))

    while (three_wall_list) != []:
        three_wall_position = three_wall_list[0]
        openable_list = openable_neighbours(maze, three_wall_position,
                                            fourty_two_list)
        print(three_wall_position, openable_list)
        for posible_opening in openable_list:
            direction = define_direction(three_wall_position,
                                         posible_opening)
            create_conexion(maze.grid[three_wall_position],
                            maze.grid[posible_opening], direction)
            if check_threexthree_area(maze) is True:
                create_wall(maze.grid[three_wall_position],
                            maze.grid[posible_opening], direction)

        three_wall_list.pop(0)

    return maze


if __name__ == "__main__":

    config = reader()

    valid_dict = parser(config)

    print(valid_dict)

    width = valid_dict.width
    height = valid_dict.height

    maze = CellMaze(width, height)

    fourty_two_list = create_42(maze)

    if valid_dict.entry in fourty_two_list:
        print("Entry can not be in 42 picture")
        sys.exit()

    if valid_dict.exit_pos in fourty_two_list:
        print("Exit can not be in 42 picture")
        sys.exit()

    initial_x, initial_y = valid_dict.entry
    initial_position = (initial_x, initial_y)

    end_x, end_y = valid_dict.exit_pos
    end_position = (end_x, end_y)

    output_file = valid_dict.output_file

    # hex_maze = create_hex_maze(maze, width, height)
    # print(hex_maze)

    perfect_maze_solution(maze, initial_x, initial_y, fourty_two_list)

    if valid_dict.perfect is False:

        not_perfect_maze_solution(maze, fourty_two_list)

    hex_maze = create_hex_maze(maze, width, height)
    bit_maze = create_bit_maze(maze, width, height)

    final_path = finding_the_way(maze, initial_position, end_position)
    print("final path:", final_path)

    with open(output_file, "w") as archive:
        for row in hex_maze:
            print("".join(row))
            archive.write("".join(row) + "\n")
        archive.write("\n")
        archive.write(f"{initial_x},{initial_y}\n")
        archive.write(f"{end_position[1]},{end_position[0]}\n")
        archive.write(f"{final_path}\n")
