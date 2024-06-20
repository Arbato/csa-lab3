import logging

import datapath

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s %(name)s %(message)s", handlers=[logging.StreamHandler()]
)


class ControlUnit:
    running = False

    def __init__(self, datapath: datapath.DataPath, program, inputs, limit=5000):
        self.datapath = datapath
        self.program = program
        self.limit = limit
        self.inputs_counter = 0
        self.inputs = inputs
        self.commands = {
            "hlt": self.hlt,
            "neg": self.neg,
            "push": self.push,
            "pop": self.pop,
            "jmp": self.jmp,
            "jz": self.jz,
            "jnz": self.jnz,
            "ld": self.ld,
            "st": self.st,
            "add": self.add,
            "sub": self.sub,
            "cmp": self.cmp,
            "inc": self.inc,
            "in": self.inn,
            "out": self.out,
            "dec": self.dec,
            "jne": self.jne,
        }
        self.save_program()

    def save_program(self):
        for row in self.program:
            if "opcode" in row and "arg" in row:
                self.datapath.memory[row["index"]] = {
                    "opcode": row["opcode"],
                    "arg": row["arg"],
                    "term": row["term"],
                    "adr": row["adr"],
                }
            elif "opcode" in row:
                self.datapath.memory[row["index"]] = {"opcode": row["opcode"], "term": row["term"]}
            else:
                self.datapath.memory[row["index"]] = {"arg": row["arg"]}

    def decode_execute(self, instruction):
        if "arg" in instruction:
            self.datapath.dr = instruction["arg"]

            if instruction["adr"] == "direct":
                arg = self.datapath.dr
                self.commands[instruction["opcode"]](arg)
                self.tick(1)

            elif instruction["adr"] == "indirect":
                arg = self.datapath.memory[self.datapath.dr]["arg"]
                self.tick(3)
                self.commands[instruction["opcode"]](arg)

            elif instruction["adr"] == "stack":
                operand = self.datapath.memory[self.datapath.dr]["arg"]
                self.tick(3)

                arg = self.datapath.memory[operand + self.datapath.sp - 1]
                self.tick(1)

                self.commands[instruction["opcode"]](arg)

            elif instruction["adr"] == "relative":
                operand = self.datapath.memory[self.datapath.dr]["arg"]
                self.tick(3)
                arg = self.datapath.memory[operand]["arg"]
                self.tick(1)

                self.commands[instruction["opcode"]](arg)

        else:
            self.commands[instruction["opcode"]]()

        logging.debug(self.datapath.__str__() + instruction["term"][2])

    def run(self):
        # Run the processor until halted
        self.running = True
        while self.running:
            instruction = self.datapath.memory[self.datapath.ar]

            self.decode_execute(instruction)
            self.datapath.ar = self.datapath.ip
            self.datapath.ip += 1
            if instruction is None :
                break  # End of program

    def tick(self, n):
        self.datapath.tick += n

    def hlt(self):
        self.running = False
        self.tick(1)

    def neg(self):
        self.datapath.acc = -self.datapath.acc
        self.datapath.set_flags()
        self.tick(1)

    def push(self):
        obj = self.datapath.acc
        self.datapath.memory[self.datapath.sp - 1] = obj
        self.datapath.sp -= 1
        self.tick(1)

    def pop(self):
        self.datapath.acc = self.datapath.memory[self.datapath.sp]
        self.datapath.sp -= 1
        self.datapath.set_flags()
        self.tick(2)

    def jmp(self, arg):
        self.datapath.ip = self.datapath.dr
        self.tick(1)

    def jz(self, arg):
        if self.datapath.Z == 1:
            self.datapath.ip = self.datapath.dr
        self.tick(1)

    def jnz(self):
        if self.datapath.Z == 0:
            self.datapath.ip = self.datapath.dr
        self.tick(1)

    def jne(self, arg):
        if self.datapath.N == 0:
            self.datapath.ip = self.datapath.dr
        self.tick(1)

    def ld(self, arg):
        self.datapath.acc = arg
        self.datapath.set_flags()
        self.tick(1)


    def st(self, arg):
        self.datapath.memory[self.datapath.dr]["arg"] = self.datapath.acc
        self.tick(2)

    def add(self, arg):
        self.datapath.acc += arg
        self.datapath.set_flags()
        self.tick(1)

    def sub(self, arg):
        self.datapath.acc -= arg
        self.datapath.set_flags()
        self.tick(1)

    def cmp(self, arg):
        try:
            self.datapath.acc -= arg
        except TypeError:
            self.datapath.acc = ord(self.datapath.acc) - arg
        self.datapath.set_flags()

        self.datapath.acc += arg
        self.tick(1)

    def inc(self, arg):
        self.datapath.memory[self.datapath.dr]["arg"] += 1
        self.datapath.acc = self.datapath.memory[self.datapath.dr]["arg"]
        self.datapath.set_flags()
        self.tick(1)

    def dec(self, arg):
        self.datapath.memory[self.datapath.dr]["arg"] -= 1
        self.datapath.acc = self.datapath.memory[self.datapath.dr]["arg"]
        self.datapath.set_flags()
        self.tick(1)

    def inn(self):
        if len(self.inputs) > self.inputs_counter:
            self.datapath.acc = ord(self.inputs[self.inputs_counter])
        self.inputs_counter += 1
        self.datapath.set_flags()
        self.tick(1)

    def out(self):
        try:
            print(chr(self.datapath.acc), end="")
        except (TypeError, ValueError):
            print(self.datapath.acc, end="")
        self.tick(1)

