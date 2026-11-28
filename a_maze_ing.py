import sys

from parser import parser, reader

from printer import printer

from pydantic import ValidationError

import MazeGenerator

from create_printable_mazes import create_hex_maze


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 a-maze-ing.py config.txt")
        sys.exit(1)

    try:
        config = reader(sys.argv[1])
        valid_dict = parser(config)

    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit(1)

    except FileNotFoundError:
        print(f"Error: Configuration file '{sys.argv[1]}' not found")
        sys.exit(1)

    except PermissionError:
        print(f"Error: Cannot read '{sys.argv[1]}'")
        sys.exit(1)

    except (ValueError, KeyError, IndexError) as e:
        print("Error: ", e)
        sys.exit(1)

    width = valid_dict.width
    height = valid_dict.height

    entry = valid_dict.entry
    exit_pos = valid_dict.exit_pos
    perfect = valid_dict.perfect

    output_file = valid_dict.output_file

    seed = valid_dict.seed

    mazegen = MazeGenerator.MazeGenerator(width,
                                          height,
                                          entry,
                                          exit_pos,
                                          perfect,
                                          output_file,
                                          seed)

    hex_maze = create_hex_maze(mazegen.maze)

    printer(hex_maze,
            mazegen.initial_position,
            mazegen.end_position, perfect)
