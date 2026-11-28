from models import CellMaze, VisitedMaze, BitMaze, HexMaze, Cell


def calculate_hex(cell: Cell) -> str:

    result = (cell.north * 1
              + cell.east * 2
              + cell.south * 4
              + cell.west * 8
              )
    return format(result, "X")


def create_hex_maze(maze: CellMaze
                    ) -> HexMaze:

    width = maze.width
    height = maze.height

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
