import numpy as np
import random
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional


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
#    print(maze[0, 0].north)
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


def create_42(visited_maze: object) -> str:

    height = maze.shape[0]
    width = maze.shape[1]

    if height < 7:
        return ("Height not enough")

    if width < 9:
        return ("Width not enough")

    x: int = int(width / 2)
    y: int = int(height / 2)

    visited_maze[y - 2, x - 3] = True
    visited_maze[y - 1, x - 3] = True
    visited_maze[y, x - 3] = True
    visited_maze[y, x - 2] = True
    visited_maze[y, x - 1] = True
    visited_maze[y + 1, x - 1] = True
    visited_maze[y + 2, x - 1] = True

    visited_maze[y - 2, x + 1] = True
    visited_maze[y - 2, x + 2] = True
    visited_maze[y - 2, x + 3] = True
    visited_maze[y - 1, x + 3] = True
    visited_maze[y, x + 3] = True
    visited_maze[y, x + 2] = True
    visited_maze[y, x + 1] = True
    visited_maze[y + 1, x + 1] = True
    visited_maze[y + 2, x + 1] = True
    visited_maze[y + 2, x + 2] = True
    visited_maze[y + 2, x + 3] = True

    return ("ok")


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

        return (self)


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
    perfect = config["PERFECT"]

    if "SEED" in config:
        seed = config["SEED"]
    else:
        seed = None

    valid_dict = Config_Dict(width=width,
                             height=height,
                             entry=initial_position,
                             exit_pos=end_position,
                             output_file=output_file,
                             perfect=perfect,
                             seed=seed
                             )

    print(valid_dict)

    maze = create_maze(width, height)
    visited_maze = create_visited_maze(width, height)
    maze_message = create_42(visited_maze)

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
