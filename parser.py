import typing

import sys

from pydantic import BaseModel, Field, model_validator, ValidationError


class Config_Dict(BaseModel):
    width: int = Field(ge=3, le=100)
    height: int = Field(ge=3, le=100)
    entry: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str = Field(max_length=100)
    perfect: bool
    seed: int | None = Field(default=None, ge=0)

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

        if not self.output_file.endswith(".txt"):
            raise ValueError("Output file must end by .txt")

        if self.output_file.startswith("."):
            raise ValueError("Output file must be in this folder")

        return (self)


def parser(config: dict[str, typing.Any]) -> Config_Dict:

    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                     "OUTPUT_FILE", "PERFECT"} 
    
    missing_keys = required_keys - config.keys()

    if missing_keys:
        raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

    except ValueError:
        raise ValueError("Width and height must be an integer")

    entry = config["ENTRY"]
    entry_list = entry.split(",")

    if len(entry_list) != 2:
        raise ValueError("ENTRY must contain exactly two coordinates (x,y)")

    initial_position_str = (entry_list[1], entry_list[0])

    try:
        initial_y = int(initial_position_str[0])
        initial_x = int(initial_position_str[1])

    except ValueError:
        raise ValueError("Initial position must be formed by integers")

    initial_position = (initial_y, initial_x)

    exit_pos = config["EXIT"]
    exit_list = exit_pos.split(",")

    if len(exit_list) != 2:
        raise ValueError("EXIT must contain exactly two coordinates (x,y)")

    end_position_str = (exit_list[1], exit_list[0])

    try:
        end_y = int(end_position_str[0])
        end_x = int(end_position_str[1])

    except ValueError:
        raise ValueError("End position must be formed by integers")

    end_position = (end_y, end_x)

    output_file = config["OUTPUT_FILE"]

    perfect_input = config["PERFECT"]

    if perfect_input == "True":
        perfect: bool = True
    elif perfect_input == "False":
        perfect = False
    else:
        raise ValueError("Invalid input: perfect must be True or False")

    if "SEED" in config and config["SEED"] != "None":
        try:
            seed: int | None = int(config["SEED"])

        except ValueError:
            raise ValueError("Seed must be None or integer")

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

    return valid_dict


def reader(input_file: str) -> dict[str, typing.Any]:

    config = {}

    with open(input_file, "r") as open_config:
        for line_number, line in enumerate(open_config, 1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid syntax at line {line_number}")

            key, value = line.split("=", 1)
            
            key = key.strip()
            value = value.strip()

            if not key or not value:
                raise ValueError(f"Empty key or value at line {line_number}")

            if key in config:
                raise ValueError(f"Duplicate configuration key: {key}")
                
            config[key] = value

            allowed_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                            "OUTPUT_FILE", "PERFECT", "SEED"}

            not_allowed_keys = config.keys() - allowed_keys

            if not_allowed_keys:
                raise ValueError(f"Unknown key: {','.join(not_allowed_keys)}")

    return config
