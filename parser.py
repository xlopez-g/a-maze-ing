import typing

import sys

from pydantic import BaseModel, Field, model_validator, ValidationError

from typing import Optional


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

        if self.entry == self.exit_pos:
            raise ValueError("Exit can not be equal entry")

        if self.output_file == "config.txt":
            raise ValueError("Do not overwrite config.txt")

        if not self.output_file.endswith("txt"):
            raise ValueError("Output file must end by .txt")

        if self.output_file.startswith("."):
            raise ValueError("Output file must be in this folder")

        return (self)


def parser(config: dict[str, typing.Any]) -> Config_Dict:

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

    except ValueError:
        print("width and height must be an integer")
        sys.exit(1)

    entry = config["ENTRY"]
    entry_list = entry.split(",")
    initial_position_str = (entry_list[1], entry_list[0])

    try:
        initial_y = int(initial_position_str[0])
        initial_x = int(initial_position_str[1])

    except ValueError:
        print("initial position must be formed by integers")
        sys.exit(1)

    initial_position = (initial_y, initial_x)

    exit_pos = config["EXIT"]
    exit_list = exit_pos.split(",")
    end_position_str = (exit_list[1], exit_list[0])

    try:
        end_y = int(end_position_str[0])
        end_x = int(end_position_str[1])

    except ValueError:
        print("End position must be formed by integers")
        sys.exit(1)

    end_position = (end_y, end_x)

    output_file = config["OUTPUT_FILE"]

    perfect_input = config["PERFECT"]

    if perfect_input == "True":
        perfect: bool = True
    elif perfect_input == "False":
        perfect = False
    else:
        raise ValueError("Invalid input: perfect must be True or False")

    if "SEED" in config:
        try:
            seed: int | None = int(config["SEED"])
    
        except ValueError:
            print("seed must be None or integer")
            sys.exit(1)

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
    
        return valid_dict

    except ValidationError as e:
        print(e.errors()[0]["msg"])
        sys.exit(1)


def reader() -> dict[str, typing.Any]:

    config = {}


    with open("config.txt", "r") as open_config:
        for line in open_config:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    
    return config