#!/usr/bin/python3
"""Транслятор Asm в машинный код.
"""

import sys

from isa import Opcode, Term, write_code

labels = {}

def get_meaningful_token(line):
    """Извлекаем из строки содержательный токен (метка или инструкция), удаляем
    комментарии и пробелы в начале/конце строки.
    """
    return line.split(";", 1)[0].strip()

# первая строка - указывает адрес начала команд

def translate_stage_1(text):
    """Первый проход транслятора. Преобразование текста программы в список
    инструкций и определение адресов меток.

    Особенность: транслятор ожидает, что в строке может быть либо 1 метка,
    либо 1 инструкция. Поэтому: `col` заполняется всегда 0, так как не несёт
    смысловой нагрузки.
    """
    code = []
    for line_num, raw_line in enumerate(text, 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue

        pc = len(code)
        if token.endswith(":"):  # токен содержит метку
            label = token.strip(":")
            assert label not in labels, "Redefinition of label: {}".format(label)
            labels[label] = pc
        elif " " in token:  # токен содержит инструкцию с операндом (отделены пробелом)
            sub_tokens = token.split(" ")
            assert len(sub_tokens) == 2, "Invalid instruction: {}".format(token)
            mnemonic, arg = sub_tokens
            opcode = Opcode(mnemonic)
            assert(opcode in Opcode.opcodes_with_arg) #  "instructions take an argument"
            code.append({"index": pc, "opcode": opcode, "arg": arg, "term": Term(line_num, 0, token)})
        else:  # токен содержит инструкцию без операндов
            opcode = Opcode(token)
            code.append({"index": pc, "opcode": opcode, "term": Term(line_num, 0, token)})

    return labels, code


def translate_stage_2(labels, code):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""
    for instruction in code:
        if "arg" in instruction:
            label = instruction["arg"]
            assert label in labels, "Label not defined: " + label
            instruction["arg"] = labels[label]
    return code


def translate(text:str):
    """Трансляция текста программы на Asm в машинный код.
    Выполняется в два прохода:

    1. Разбор текста на метки и инструкции.

    2. Подстановка адресов меток в операнды инструкции.
    """

    labels, code = translate_stage_1(text)
    
    code = translate_stage_2(labels, code)

    # ruff: noqa: RET504
    return code


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

def trimmer(code):
    result = []
    for line in code:
        if ";" in line:
            line = line[: line.index(";")]
        line = line.strip()
        if line:
            result.append(line)
    return result

def translate_data(data: list):
    

def main(source: str, target: str):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    with open(source, encoding="utf-8") as f:
        source = f.read().split("\n")

    source = trimmer(source)
    data, code = section_split(source)
    data = translate_data(data)

    code = translate(code)

    write_code(target, code)
    print("source LoC:", len(source.split("\n")), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator_asm.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)