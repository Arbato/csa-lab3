from isa import Opcode, read_code
from datapath import DataPath
from control_unit import ControlUnit
import sys

def main(code_file, input_file):
    """ Function for running maachine using control unit
    """
    code = read_code(code_file)
    with open(input_file, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)
            
        input_token.append('\0')

    data_path = DataPath()
    control_unit = ControlUnit(data_path, code, input_token)
    control_unit.run()

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: machine.py <translated_code.json> <input_data>"
    _, code, input = sys.argv 
    main(code, input)