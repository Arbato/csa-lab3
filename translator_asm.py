import sys

from isa import Opcode, Term, write_code

labels = {}

def trimmer(code):
    result = []
    for line in code:
        if ";" in line:
            line = line[: line.index(";")]
        line = line.strip()
        if line:
            result.append(line)
    return result

def section_split(source):
    data, code = [], []
    section = None
    for line in source:
        if ".data" in line:
            section = data
        elif ".instructions" in line:
            section = code
        elif section is not None:
            section.append(line)
    print(data, code)
    return data, code

def translate_stage_1_data(data: list):




def translate():
    data, code = section_split(source)
    


def main(source: str, target: str):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    with open(source, encoding="utf-8") as f:
        source = f.read().split("\n")

    source = trimmer(source)
    

    write_code(target, code)
    print("source LoC:", len(source), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator_asm.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)