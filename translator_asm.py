import sys

from isa import Opcode, Term, write_code

labels = {}


def get_meaningful_token(line):
    """Извлекаем из строки содержательный токен (метка или инструкция), удаляем
    комментарии и пробелы в начале/конце строки.
    """
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
    print(data, code)
    return data, code

def translate_stage_1(data, text):
    code = []
    for line_num, raw_line in enumerate(text, 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue

        pc = len(code)+len(data)
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
            if '$' in arg:
                try:

                    code.append({"index": pc, "opcode": opcode, "arg": int(arg.strip("$")), "term": Term(line_num, 0, token), "direct": True})
                except ValueError:
                    code.append({"index": pc, "opcode": opcode, "arg": arg.strip("$"), "term": Term(line_num, 0, token), "direct": True})
                    print(arg.strip("$"))

            else:
                code.append({"index": pc, "opcode": opcode, "arg": arg, "term": Term(line_num, 0, token), "direct": False})
        else:  # токен содержит инструкцию без операндов
            opcode = Opcode(token)
            code.append({"index": pc, "opcode": opcode, "term": Term(line_num, 0, token), "direct": False})

    return code

def translate_stage_2(labels, code: list):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""
    for instruction in code:
        if "arg" in instruction:
            label = instruction["arg"]
            if instruction["direct"]==False or isinstance(label, str):
                assert label in labels, "Label not defined: " + label
                instruction["arg"] = labels[label]
    return code




def data_translate_stage_1(text):
    """
    converts data that looks like
    ["int: 123",
    "msg: "hi""
    ]
    to 
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

        pc = len(code)+1
        if ":" in token:
            if "\"" in token:  # data is a string
                sub_tokens  = token.split(": ")
                assert len(sub_tokens) == 2, "Invalid data entry: {}".format(token)

                label, string = sub_tokens
                assert label not in labels, "Redefinition of label: {}".format(label)
                labels[label] = pc
                string = string.strip("\"")
                length = len(string)
                code.append({"index": pc, "arg": length})
                for letter in string:
                    pc = len(code)+1
                    code.append({"index": pc, "arg": letter })
        
        
            elif " " in token:  # data is an int
                sub_tokens = token.split(": ")
                assert len(sub_tokens) == 2, "Invalid instruction: {}".format(token)
                label, arg = sub_tokens
                labels[label] = pc

                code.append({"index": pc, "arg": arg})
            print(token, code,  "\n")



    code.insert(0, {"index": 0, "opcode": "jmp",  "arg": len(code)+1 })

    print(labels, code,  "\n")
    return code
    


def translate(source: list):
    data, code = section_split(source)
    print("section splity data+code")
    print (data)
    print(code)
    data = data_translate_stage_1(data)
    code = translate_stage_1(data, code)

    print("data+code after 1 stage")
    print(data )
    print(code)

    print()
    print("labels")
    print (labels)


    full_code = translate_stage_2(labels, code)
    return data+full_code


def main(source: str, target: str):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    with open(source, encoding="utf-8") as f:
        lines = f.read().split("\n")
    lines = trimmer(lines)
    code = translate(lines)
    print("code in main ", code, "\n")
    write_code(target, code)
    print("source LoC:", len(source), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator_asm.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)



   