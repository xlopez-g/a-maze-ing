import random

from models import CellMaze, VisitedMaze

from directions import define_direction, short_direction, create_wall, create_conexion, three_wall_cells

from neighbours import openable_neighbours
from neighbours import check_open_neighbours
from neighbours import check_valid_neighbours

from create_printable_mazes import create_hex_maze


class MazeGenerator:

    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit_pos: tuple[int, int],
                 perfect: bool,
                 output_file,
                 seed: int | None) -> None:

        self.width = width
        self.height = height
        self.entry = entry
        self.exit_pos = exit_pos
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed

        initial_x, initial_y = self.entry
        self.initial_position = (initial_y, initial_x)

        end_x, end_y = self.exit_pos
        self.end_position = (end_y, end_x)

        self.forty_two_list: list[tuple[int, int]] = []

        self.maze: CellMaze = CellMaze(width, height)

        self.final_path: list[tuple[int, int]] | None = None

        self.generator()

    def reading_the_dict(self,
                         parents_dict: dict[tuple[int, int], tuple[int, int]]
                         ) -> str:

        initial_position = self.initial_position
        end_position = self.end_position

        path = [end_position]

        step = end_position

        while step != initial_position:
            if step not in parents_dict:
                raise ValueError("No path between entry and exit")

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

    def finding_the_way(self) -> str:

        maze = self.maze
        initial_position = self.initial_position
        end_position = self.end_position

        height = maze.height
        width = maze.width

        visited_maze = VisitedMaze(width, height)

        queue = [initial_position]
        parents_dict: dict[tuple[int, int], tuple[int, int]] = {}

        while (queue):
            visited_maze.grid[queue[0]] = True

            valid_neighbours = check_open_neighbours(maze,
                                                     queue[0][0],
                                                     queue[0][1])
            not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                      if visited_maze.grid[neighbours] is False]

            for neighbour in not_visited_neighbours:
                parents_dict.update({neighbour: queue[0]})

            if end_position in not_visited_neighbours:
                break

            queue.pop(0)
            for member in not_visited_neighbours:
                queue.append(member)
                visited_maze.grid[member] = True

        final_path = self.reading_the_dict(parents_dict)

        return (final_path)

    def create_42(self) -> list[tuple[int, int]]:

        maze = self.maze

        height = maze.height
        width = maze.width

        if height < 7:
            print("Height not enough for 42 picture")
            forty_two_list: list[tuple[int, int]] = []

        elif width < 9:
            print("Width not enough for 42 picture")
            forty_two_list = []

        else:

            x = width // 2
            y = height // 2

            forty_two_list = [(y - 2, x - 3), (y - 1, x - 3), (y, x - 3),
                              (y, x - 2), (y, x - 1),
                              (y + 1, x - 1), (y + 2, x - 1),
                              (y - 2, x + 1), (y - 2, x + 2),
                              (y - 2, x + 3), (y - 1, x + 3), (y, x + 3),
                              (y, x + 2), (y, x + 1), (y + 1, x + 1),
                              (y + 2, x + 1), (y + 2, x + 2),
                              (y + 2, x + 3)
                              ]

        return forty_two_list

    def open_corners(self) -> None:

        maze: CellMaze = self.maze

        height = maze.height
        width = maze.width

        if maze.grid[0, 0].south != 0:
            direction = define_direction((0, 0), (1, 0))
            create_conexion(maze.grid[0, 0], maze.grid[1, 0], direction)

        if maze.grid[0, 0].east != 0:
            direction = define_direction((0, 0), (0, 1))
            create_conexion(maze.grid[0, 0], maze.grid[0, 1], direction)

        if maze.grid[height - 1, 0].north != 0:
            cell = maze.grid[height - 1, 0]
            cell_next = maze.grid[height - 2, 0]
            direction = define_direction((height - 1, 0), (height - 2, 0))
            create_conexion(cell, cell_next, direction)

        if maze.grid[height - 1, 0].east != 0:
            cell = maze.grid[height - 1, 0]
            cell_next = maze.grid[height - 1, 1]
            direction = define_direction((height - 1, 0), (height - 1, 1))
            create_conexion(cell, cell_next, direction)

        if maze.grid[0, width - 1].south != 0:
            cell = maze.grid[0, width - 1]
            cell_next = maze.grid[1, width - 1]
            direction = define_direction((0, width - 1), (1, width - 1))
            create_conexion(cell, cell_next, direction)

        if maze.grid[0, width - 1].west != 0:
            cell = maze.grid[0, width - 1]
            cell_next = maze.grid[0, width - 2]
            direction = define_direction((0, width - 1), (0, width - 2))
            create_conexion(cell, cell_next, direction)

        border = (height - 1, width - 1)
        if maze.grid[border].north != 0:
            cell = maze.grid[height - 2, width - 1]
            cell_next = maze.grid[border]
            direction = define_direction((height - 2, width - 1), border)
            create_conexion(cell, cell_next, direction)

        if maze.grid[border].west != 0:
            cell = maze.grid[border]
            cell_next = maze.grid[height - 1, width - 2]
            direction = define_direction(border, (height - 1, width - 2))
            create_conexion(cell, cell_next, direction)

    def check_zero_around(self,
                          position: tuple[int, int]
                          ) -> bool:

        maze = self.maze

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

    def check_threexthree_area(self) -> bool:

        maze = self.maze

        result = False
        height = maze.height
        width = maze.width

        for x in range(1, width - 1):
            for y in range(1, height - 1):
                cell = maze.grid[y, x]
                cell_sum = cell.north + cell.east + cell.south + cell.west
                if cell_sum == 0:
                    if self.check_zero_around((y, x)):
                        return True

        return (result)

    def perfect_maze_solution(self) -> CellMaze:

        maze = self.maze
        initial_position = self.initial_position
        seed = self.seed
        forty_two_list = self.forty_two_list

        height = maze.height
        width = maze.width

        initial_x = initial_position[1]
        initial_y = initial_position[0]

        rng = random.Random(seed)

        visited_maze = VisitedMaze(width, height)
        visited_list = [(initial_y, initial_x)]

        visited_maze.grid[initial_y, initial_x] = True

        for y_coord, xcoord in forty_two_list:
            visited_maze.grid[y_coord, xcoord] = True

        while visited_list:

            y = visited_list[-1][0]
            x = visited_list[-1][1]

            valid_neighbours = check_valid_neighbours(maze, (y, x))

            not_visited_neighbours = [neighbours for neighbours in valid_neighbours
                                      if visited_maze.grid[neighbours] is False]

            if not_visited_neighbours:

                next_cell = rng.choice(not_visited_neighbours)
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

    def not_perfect_maze_solution(self) -> CellMaze:

        maze = self.maze
        forty_two_list = self.forty_two_list

        height = maze.height
        width = maze.width

        self.open_corners()

        three_wall_list = three_wall_cells(self.maze)
        center_x: int = width // 2
        center_y: int = height // 2

        if forty_two_list != []:
            if (center_y - 1, center_x + 2) in forty_two_list:
                three_wall_list.remove((center_y - 1, center_x + 2))
            if (center_y + 1, center_x + 2) in forty_two_list:
                three_wall_list.remove((center_y + 1, center_x + 2))

        while (three_wall_list) != []:
            three_wall_position = three_wall_list[0]
            openable_list = openable_neighbours(maze, three_wall_position,
                                                forty_two_list)
            print(three_wall_position, openable_list)
            for possible_opening in openable_list:
                direction = define_direction(three_wall_position,
                                             possible_opening)
                create_conexion(maze.grid[three_wall_position],
                                maze.grid[possible_opening], direction)
                if self.check_threexthree_area() is True:
                    create_wall(maze.grid[three_wall_position],
                                maze.grid[possible_opening], direction)

            three_wall_list.pop(0)

        return maze

    def generator(self) -> CellMaze:

        self.forty_two_list = self.create_42()

        if self.initial_position in self.forty_two_list:
            raise ValueError("Entry can not be in 42 picture")

        if self.end_position in self.forty_two_list:
            raise ValueError("Exit can not be in 42 picture")

        self.perfect_maze_solution()

        if self.perfect is False:

            self.not_perfect_maze_solution()

        final_path = self.finding_the_way()

        hex_maze = create_hex_maze(self.maze)

        initial_x = self.initial_position[1]
        initial_y = self.initial_position[0]

        with open(self.output_file, "w") as archive:
            hex_printer: str = ""
            for row in hex_maze:
                hex_printer += ("".join(row))
                hex_printer += "\n"
                archive.write("".join(row) + "\n")
            archive.write("\n")
            archive.write(f"{initial_x},{initial_y}\n")
            archive.write(f"{self.end_position[1]},{self.end_position[0]}\n")
            archive.write(f"{final_path}\n")

        return (self.maze)
