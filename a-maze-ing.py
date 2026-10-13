import numpy as np
import random
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional
import sys


class Cell:
    def __init__(self):
        self.north = 1
        self.east = 1
        self.south = 1
        self.west = 1


def create_visited_maze(width: int, height: int) -> object:

    visited_maze = np.empty((height, width), dtype=object)

    for column in range(width):
        for row in range(height):
            visited_maze[row, column] = False
    return visited_maze


def create_maze(width: int, height: int) -> object:

    maze = np.empty((height, width), dtype=object)

    for column in range(width):
        for row in range(height):
            maze[row, column] = Cell()
    return maze


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


def create_hex_maze(maze: object, width: int, height: int) -> object:

    hex_maze = np.empty((height, width), dtype=object)

    for x in range(width):
        for y in range(height):
            hex_maze[y, x] = calculate_hex(maze[y, x])
#    print(maze[0, 0].north)
    return hex_maze


def create_bit_maze(maze: object, width: int, height: int) -> object:

    bit_maze = np.empty((height, width), dtype=int)

    for x in range(width):
        for y in range(height):
            bit_maze[y, x] = (maze[y, x].north * 1
                              + maze[y, x].east * 10
                              + maze[y, x].south * 100
                              + maze[y, x].west * 1000
                              )

    return bit_maze


def create_conexion(cell1: Cell, cell2: Cell, direction) -> None:
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


def create_wall(cell1: Cell, cell2: Cell, direction) -> None:
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


def check_valid_neighbours(maze: object, y: int, x: int) -> list:
    height = maze.shape[0]
    width = maze.shape[1]

    neighbour_list = []

    if x > 0:
        neighbour1 = y, x - 1
        neighbour_list.append(neighbour1)
    if x < width - 1:
        neighbour2 = y, x + 1
        neighbour_list.append(neighbour2)
    if y > 0:
        neighbour3 = y - 1, x
        neighbour_list.append(neighbour3)
    if y < height - 1:
        neighbour4 = y + 1, x
        neighbour_list.append(neighbour4)
    return neighbour_list


def openable_neighbours(maze: object, position: tuple[int, int],
                        fourty_two_list: list[tuple[int, int]]) -> list:
    height = maze.shape[0]
    width = maze.shape[1]

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


def check_open_neighbours(maze: object, y: int, x: int) -> list:
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


def reading_the_dict(parents_dict: dict, end_position: tuple[int, int]) -> str:

    path = [end_position]

    while end_position != (0, 0):
        temp = parents_dict[end_position]
    #    print(temp)
        path.append(temp)
        end_position = temp

    # print("path:", path)
    # print("len(path)", len(path))

    result = ""

    for position_number in range((len(path)) - 1):
        initial_position = path[len(path) - position_number - 1]
        next_position = path[len(path) - position_number - 2]
        direction = short_direction(initial_position, next_position)
        result += direction

    return result


def finding_the_way(maze: object, init: tuple[int, int],
                    end: tuple[int, int]) -> str:

    height = maze.shape[0]
    width = maze.shape[1]

    visited_maze = create_visited_maze(width, height)

    qeue = [init]
    parents_dict = {}

    while (qeue):
        visited_maze[qeue[0]] = True

        valid_neighbours = check_open_neighbours(maze, qeue[0][0], qeue[0][1])
        not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                  if visited_maze[neighbours] is False]

        for neighbour in not_visited_neighbours:
            parents_dict.update({neighbour: qeue[0]})

        if end in not_visited_neighbours:
            break

        qeue.pop(0)
        for member in not_visited_neighbours:
            qeue.append(member)
            visited_maze[member] = True

    final_path = reading_the_dict(parents_dict, end)

    return (final_path)


def create_42(visited_maze: object) -> list[list[int, int]]:

    height = visited_maze.shape[0]
    width = visited_maze.shape[1]

    x: int = int(width / 2)
    y: int = int(height / 2)

    fourty_two_list = [(y - 2, x - 3), (y - 1, x - 3), (y, x - 3), (y, x - 2),
                       (y, x - 1), (y + 1, x - 1), (y + 2, x - 1),
                       (y - 2, x + 1), (y - 2, x + 2), (y - 2, x + 3),
                       (y - 1, x + 3), (y, x + 3), (y, x + 2), (y, x + 1),
                       (y + 1, x + 1), (y + 2, x + 1), (y + 2, x + 2),
                       (y + 2, x + 3)
                       ]

    for y_coord, xcoord in fourty_two_list:
        visited_maze[y_coord, xcoord] = True

    return fourty_two_list


class Config_Dict(BaseModel):
    width: int = Field(ge=3, le=100)
    height: int = Field(ge=3, le=100)
    entry: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str = Field(max_length=100)
    perfect: bool
    seed: Optional[int] = None

    @model_validator(mode='after')
    def parameter_checker(self) -> 'Config_Dict':
        if self.entry[0] >= self.height or self.entry[0] < 0:
            raise ValueError("Entry parameter out of range")

        if self.entry[1] >= self.width or self.entry[1] < 0:
            raise ValueError("Entry parameter out of range")

        if self.exit_pos[0] >= self.height or self.exit_pos[0] < 0:
            raise ValueError("Exit parameter out of range")

        if self.exit_pos[1] >= self.width or self.exit_pos[1] < 0:
            raise ValueError("Exit parameter out of range")

        if entry == exit_pos:
            raise ValueError("Exit can not be equal entry")

        if output_file == "config.txt":
            raise ValueError("Do not overwrite config.txt")

        if not output_file.endswith("txt"):
            raise ValueError("Output file must end by .txt")

        if output_file.startswith("."):
            raise ValueError("Output file must be in this folder")

        return (self)


def three_wall_cells(maze: object) -> list[tuple[int, int]]:
    three_wall_list = []

    height = visited_maze.shape[0]
    width = visited_maze.shape[1]

    for x in range(width):
        for y in range(height):
            cell = maze[y, x]
            if (cell.north + cell.east + cell.south + cell.west) == 3:
                three_wall_list.append((y, x))

    print("lista d 3paredes", three_wall_list)

    return (three_wall_list)


def open_corners(maze) -> None:

    height = maze.shape[0]
    width = maze.shape[1]

    if maze[0, 0].south != 0:
        create_conexion(maze[0, 0], maze[1, 0], "south")
    if maze[0, 0].west != 0:
        create_conexion(maze[0, 0], maze[0, 1], "east")

    if maze[height - 1, 0].north != 0:
        create_conexion(maze[height - 1, 0], maze[height - 2, 0], "north")
    if maze[height - 1, 0].west != 0:
        create_conexion(maze[height - 1, 0], maze[height - 1, 1], "east")

    if maze[0, width - 1].south != 0:
        create_conexion(maze[0, width - 1], maze[1, width - 1], "south")
    if maze[0, width - 1].east != 0:
        create_conexion(maze[0, width - 1], maze[0, width - 2], "west")

    if maze[height - 1, width - 1].north != 0:
        create_conexion(maze[height - 2, width - 1],
                        maze[height - 1, width - 1], "south")
    if maze[height - 1, width - 1].east != 0:
        create_conexion(maze[height - 1, width - 1],
                        maze[height - 1, width - 2], "west")


def check_zero_around(maze, position: tuple[int, int]) -> bool:
    y = position[0]
    x = position[1]

    result = True

    if maze[y - 1, x - 1].south != 0 or maze[y - 1, x - 1].east != 0:
        return (False)

    if maze[y + 1, x - 1].north != 0 or maze[y + 1, x - 1].east != 0:
        return (False)

    if maze[y - 1, x + 1].south != 0 or maze[y - 1, x + 1].west != 0:
        return (False)

    if maze[y + 1, x + 1].north != 0 or maze[y + 1, x + 1].west != 0:
        return (False)

    return (result)


def check_threexthree_area(maze) -> bool:
    result = False
    height = maze.shape[0]
    width = maze.shape[1]

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            cell = maze[y, x]
            cell_sum = cell.north + cell.east + cell.south + cell.west
            if cell_sum == 0:
                if check_zero_around(maze, (y, x)):
                    return True

    return (result)


if __name__ == "__main__":

    config = {}
    with open("config.txt", "r") as open_config:
        for line in open_config:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])

    entry = config["ENTRY"]
    entry_list = entry.split(",")
    initial_position_str = (entry_list[1], entry_list[0])
    initial_y = int(initial_position_str[0])
    initial_x = int(initial_position_str[1])

    initial_position = (initial_y, initial_x)

    exit_pos = config["EXIT"]
    exit_list = exit_pos.split(",")
    end_position_str = (exit_list[1], exit_list[0])
    end_y = int(end_position_str[0])
    end_x = int(end_position_str[1])

    end_position = (end_y, end_x)

    output_file = config["OUTPUT_FILE"]
    perfect: bool = config["PERFECT"]

    if "SEED" in config:
        seed = config["SEED"]
    else:
        seed = None

    try:
        valid_dict = Config_Dict(width=width,
                                 height=height,
                                 entry=initial_position,
                                 exit_pos=end_position,
                                 output_file=output_file,
                                 perfect=perfect,
                                 seed=seed
                                 )

    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit()

    print(valid_dict)

    maze = create_maze(width, height)
    visited_maze = create_visited_maze(width, height)

    fourty_two_bool = False

    if height < 7:
        print("Height not enough for 42 picture")
        fourty_two_list = []

    elif width < 9:
        print("Width not enough for 42 picture")
        fourty_two_list = []

    else:
        fourty_two_bool = True
        fourty_two_list = create_42(visited_maze)

    if valid_dict.entry in fourty_two_list:
        print("Entry can not be in 42 picture")
        sys.exit()

    if valid_dict.exit_pos in fourty_two_list:
        print("Exit can not be in 42 picture")
        sys.exit()

    visited_maze[initial_y, initial_x] = True
    visited_list = [(initial_y, initial_x)]
    # hex_maze = create_hex_maze(maze, width, height)
    # print(hex_maze)

    while visited_list:

        y = visited_list[-1][0]
        x = visited_list[-1][1]

        valid_neighbours = check_valid_neighbours(maze, y, x)
        not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                  if visited_maze[neighbours] is False]

        if not_visited_neighbours:
            next_cell = random.choice(not_visited_neighbours)
            visited_list.append(next_cell)

            next_x = next_cell[1]
            next_y = next_cell[0]

            direction = define_direction((y, x), (next_y, next_x))

            create_conexion(maze[y, x], maze[next_y, next_x], direction)
            visited_maze[next_cell[0], next_cell[1]] = True

        else:
            visited_list.pop()

    if valid_dict.perfect is False:
        open_corners(maze)

        three_wall_list = three_wall_cells(maze)
        center_x: int = int(width / 2)
        center_y: int = int(height / 2)

        if fourty_two_bool:
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
                create_conexion(maze[three_wall_position],
                                maze[posible_opening], direction)
                if check_threexthree_area is True:
                    create_wall(three_wall_position,
                                posible_opening, direction)

            three_wall_list.pop(0)

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
