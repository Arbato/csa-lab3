import sys

from control_unit import ControlUnit
from datapath import DataPath
from isa import read_code


def main(code, input_token):
    """Function for running maachine using control unit"""

    data_path = DataPath()
    control_unit = ControlUnit(data_path, code, input_token)
    control_unit.run()


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: machine.py <translated_code.json> <input_data>"
    _, code, inputs = sys.argv
    code = read_code(code)
    with open(inputs, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)

        input_token.append("\0")
    main(code, input_token)
