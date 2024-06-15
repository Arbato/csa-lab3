import json
from collections import namedtuple
from enum import Enum


class Opcode(str, Enum):
    HLT = "hlt"
    NEG = "neg"
    PUSH = "push"
    POP = "pop"
    JMP = "jmp"
    JZ = "jz"
    JNZ = "jnz"
    JNE = "jne"
    LD = "ld"
    LDSP = "ldsp"
    ST = "st"
    ADD = "add"
    SUB = "sub"
    OR = "or"
    AND = "and"
    CMP = "cmp"
    INC = "inc"
    IN = "in"
    OUT = "out"
    ALD = "ald"
    DEC = "dec"
    
    opcodes_with_arg = {PUSH,POP, JMP, JZ, JNZ, LD, ST, ADD, SUB, OR, AND,  CMP, INC, DEC, JNE}
    direct_opcodes  = {JMP, JZ, INC, DEC, JNE}


    def __str__(self):
        """Переопределение стандартного поведения `__str__` для `Enum`: вместо
        `Opcode.INC` вернуть `increment`.
        """
        return str(self.value)


class Term(namedtuple("Term", "line pos symbol")):
    """Описание выражения из исходного текста программы.

    Сделано через класс, чтобы был docstring.
    """


def write_code(filename, code):
    """Записать машинный код в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        # Почему не: `file.write(json.dumps(code, indent=4))`?
        # Чтобы одна инструкция была на одну строку.
        buf = []
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename):
    """Прочесть машинный код из файла.

    Так как в файле хранятся не только простейшие типы (`Opcode`, `Term`), мы
    также выполняем конвертацию в объекты классов вручную (возможно, следует
    переписать через `JSONDecoder`, но это скорее усложнит код).
    """
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())

    return code