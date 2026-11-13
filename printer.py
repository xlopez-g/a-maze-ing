from models import HexMaze, PrintMaze, COLORS

import random


def printer(hex_maze: HexMaze,
            initial_position: tuple[int, int],
            end_position: tuple[int, int]):

    simple_square = "\u2588"

    width = hex_maze.width 
    height = hex_maze.height

    Nx = width * 2 + 1
    Ny = height * 2 + 1

    print_maze = PrintMaze(Nx, Ny)


    for x in range(0, width):
        for y in range(height):
            print_maze.grid[y * 2 + 1, x * 2 + 1] = " "

    
    for x in range(0, width):
        for y in range(height):
            if hex_maze.grid[y, x] in ("0", "1", "4", "5", "8", "9", "D", "C"):
                print_maze.grid[y * 2 + 1, x * 2 + 2] = " "
            if hex_maze.grid[y, x] in ("0", "1", "2", "3", "8", "9", "A", "B"):
                print_maze.grid[y * 2 + 2, x * 2 + 1] = " "
      #      if hex_maze.grid[y, x] in ("C", "A", "6", "E"):
       #         print_maze.grid[y * 2, x * 2 + 1] = " "
        #    if hex_maze.grid[y, x] in ("5", "3", "7", "6"):
         #       print_maze.grid[y * 2 + 1, x * 2] = " "
    
    
    grid = print_maze.grid
    for x in range(0, Nx, 2):
        for y in range(0, Ny, 2):
            
            up = grid[y - 1, x] if y > 0 else " "
            down = grid[y + 1, x] if y < Ny - 1 else " "
            left = grid[y, x - 1] if x > 0 else " "
            right = grid[y, x + 1] if x < Nx - 1 else " "

            if (up == "┃"
                and down == "┃"
                and left == "━"
                and right == "━"):
                grid[y, x] = "╋"

            elif (up == " "
                  and down == "┃"
                  and left == "━"
                  and right == "━"):
                grid[y, x] = "┳"

            elif (up == "┃"
                  and down == " "
                  and left == "━"
                  and right == "━"):
                grid[y, x] = "┻"

            elif (up == "┃"
                  and down == "┃"
                  and left == " "
                  and right == "━"):
                grid[y, x] = "┣"

            elif (up == "┃"
                  and down == "┃"
                  and left == "━"
                  and right == " "):
                grid[y, x] = "┫"

            elif (up == "┃"
                  and down == " "
                  and left == "━"
                  and right == " "):
                grid[y, x] = "┛"

            elif (up == "┃"
                  and down == " "
                  and left == " "
                  and right == "━"):
                grid[y, x] = "┗"

            elif (up == " "
                  and down == "┃"
                  and left == " "
                  and right == "━"):
                grid[y, x] = "┏"

            elif (up == " "
                  and down == "┃"
                  and left == "━"
                  and right == " "):
                grid[y, x] = "┓"

            elif (up == "┃"
                  and down == "┃"
                  and left == " "
                  and right == " "):
                grid[y, x] = "┃"

            elif (up == " "
                  and down == " "
                  and left == "━"
                  and right == "━"):
                grid[y, x] = "━"
   
    maze_printer = ""
    for row in print_maze:
        maze_printer += "".join(row)
        maze_printer += "\n"

    color = random.choice(list(COLORS))

    print(color.value, maze_printer, COLORS.reset.value, sep="")

    '''
    for y in range(0, Ny):
        if y % 2 == 0:
            for x in range(0, Nx):
                if x % 2 == 0 or y == 0:
                    print(simple_square, end="")
                else:
                    print(" ", end="")
            print()
        else:
#            print(simple_square, end=""):
 #           if hex_maze.grid[y, x] in ("9", "C", "5", "D")
  #              print(derecha)
            print(simple_square)

    '''
