import sys

from isa import Opcode, Term, write_code

labels = {}


def get_meaningful_token(line):
    """Избавление от комментариев"""
    return line.split(";", 1)[0].strip()


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
    return data, code


def clean_code(code):
    if "$" in code["arg"] or code["opcode"] in Opcode.direct_opcodes:
        code["adr"] = "direct"
        try:
            code["arg"] = int(code["arg"].strip("$"))
        except ValueError:
            code["arg"] = code["arg"].strip("$")

    elif "@" in code["arg"]:
        code["adr"] = "stack"
        try:
            code["arg"] = int(code["arg"].strip("@"))
        except ValueError:
            code["arg"] = code["arg"].strip("@")
    elif "#" in code["arg"]:
        code["adr"] = "relative"
        try:
            code["arg"] = int(code["arg"].strip("#"))
        except ValueError:
            code["arg"] = code["arg"].strip("#")
    else:
        code["adr"] = "indirect"

    return code


def translate_stage_1(data, text):
    code = []
    for line_num, raw_line in enumerate(text, 1):
        token = raw_line
        if token == "":
            continue

        pc = len(code) + len(data)
        if token.endswith(":"):  # токен содержит метку
            label = token.strip(":")
            assert label not in labels, "Redefinition of label: {}".format(label)
            labels[label] = pc

        elif " " in token:  # токен содержит инструкцию с операндом (отделены пробелом)
            sub_tokens = token.split(" ")
            assert len(sub_tokens) == 2, "Invalid instruction: {}".format(token)
            mnemonic, arg = sub_tokens
            opcode = Opcode(mnemonic)
            assert opcode in Opcode.opcodes_with_arg

            code.append(clean_code({"index": pc, "opcode": opcode, "arg": arg, "term": Term(line_num, 0, token)}))

        else:  # токен содержит инструкцию без операндов
            opcode = Opcode(token)
            code.append({"index": pc, "opcode": opcode, "term": Term(line_num, 0, token), "adr": "indirect"})

    return code


def translate_stage_2(labels, code: list):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""
    for instruction in code:
        if "arg" in instruction:
            label = instruction["arg"]
            if "adr" in instruction:
                if instruction["adr"] != "direct" or isinstance(label, str):
                    assert label in labels, "Label not defined: " + label
                    instruction["arg"] = labels[label]

            elif isinstance(label, str):
                instruction["arg"] = labels[label]
    return code


def data_translate_stage_1(text):
    """

    Конвертирует данные из вида
    ["int: 123",
    "msg: "hi""
    ]
    в такой вид:
    [{index 0, opcode: "jmp",  arg: 5 },
     {index 1, arg: 123 },
     {index 2, arg: 2},
     {index 3, arg: "h"},
     {index 4, arg: "i"}
     ]"""

    code = []
    for line_num, raw_line in enumerate(text, 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue

        pc = len(code) + 1
        if ":" in token:
            if '"' in token:  # data is a string
                sub_tokens = token.split(": ")
                assert len(sub_tokens) == 2, "Invalid data entry: {}".format(token)

                label, string = sub_tokens
                assert label not in labels, "Redefinition of label: {}".format(label)
                labels[label] = pc
                string = string.strip('"')
                length = len(string)
                code.append({"index": pc, "arg": length})
                for letter in string:
                    pc = len(code) + 1
                    code.append({"index": pc, "arg": letter})

            elif " " in token:  # data is an int
                sub_tokens = token.split(": ")
                assert len(sub_tokens) == 2, "Invalid instruction: {}".format(token)
                label, arg = sub_tokens
                labels[label] = pc

                code.append({"index": pc, "arg": int(arg)})

    code.insert(
        0,
        {
            "index": 0,
            "opcode": "jmp",
            "arg": len(code) + 1,
            "term": Term(line_num, 0, "Jump to start"),
            "adr": "direct",
        },
    )

    return code


def translate(source: list):
    data, code = section_split(source)

    data = data_translate_stage_1(data)
    code = translate_stage_1(data, code)

    full_code = translate_stage_2(labels, code)
    return data + full_code


def main(source: str, target: str):
    """Функция запуска транслятора. Параметры -- p."""
    with open(source, encoding="utf-8") as f:
        lines = f.read().split("\n")
    lines = trimmer(lines)
    code = translate(lines)
    write_code(target, code)
    print("source LoC:", len(lines), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator_asm.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)
