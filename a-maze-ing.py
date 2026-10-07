import numpy as np
import random


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

def create_maze(width, height) -> object:
 
    maze = np.empty((height, width), dtype=object)

    for column in range(width):
        for row in range(height):
            maze[row, column] = Cell()
#    print(maze[0, 0].north)
    return maze


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
            bit_maze[y, x] = maze[y, x].north * 1000 + maze[y, x].east * 100 + maze[y, x].south * 10 + maze[y, x].west * 1
#    print(maze[0, 0].north)
    return bit_maze


def create_conexion(cell1: Cell, cell2:Cell, direction) -> None:
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
    
    
def check_valid_neighbours(maze: object, x: int, y: int) -> list:
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
         




if __name__ == "__main__":
    width = 3
    height = 10
    maze = create_maze(width, height)
    visited_maze = create_visited_maze(width, height)
    #inicial position = 0, 0
    initial_x = 0
    initial_y = 0
    initial_position = (initial_y, initial_x)
    visited_maze[initial_y, initial_x] = True
    visited_list = [(initial_y, initial_x)]
    # hex_maze = create_hex_maze(maze, width, height)
    # print(hex_maze)

    while visited_list:
        
        x = visited_list[-1][1]
        y = visited_list[-1][0]
    
        valid_neighbours = check_valid_neighbours(maze, x , y)
        not_visited_neighbours = [neighbours for neighbours in valid_neighbours if visited_maze[neighbours] is False]
        
        if not_visited_neighbours:
            next_cell = random.choice(not_visited_neighbours)
            visited_list.append(next_cell)

            print(next_cell)

            next_x = next_cell[1]
            next_y = next_cell[0]

            if y - next_y == -1:
                direction = "south"
            elif y - next_y == 1:
                direction = "north"
            elif x - next_x == -1:
                direction = "west"
            elif x - next_x == 1 :
                direction = "east"

            create_conexion(maze[y, x], maze[next_y, next_x], direction)
            visited_maze[next_cell[0], next_cell[1]] = True
            #print(visited_maze)
            #print(visited_list)
        else:
            visited_list.pop()
    print(visited_list)
    print(visited_maze)

    hex_maze = create_hex_maze(maze, width, height)
    print(hex_maze)
    bit_maze = create_bit_maze(maze, width, height)
    print(bit_maze)
    print("north", maze[0,0].north)
    print("east", maze[0,0].east)
    print("south", maze[0,0].south)
    print("west", maze[0,0].west)