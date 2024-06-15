from datapath import DataPath
import logging


logging.basicConfig(
    level = logging.DEBUG,
    format = "%(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler()]
)


class ControlUnit:
    running = False

    def __init__(self, datapath: DataPath, program, inputs, limit = 5000):
        self.datapath = datapath
        self.program = program
        self.limit = limit
        self.instr_counter = 0
        self.inputs = inputs
        self.commands = {"hlt": self.hlt, 
                "neg": self.neg,
                "push": self.push,
                "pop": self.pop,
                "jmp": self.jmp,
                "jz": self.jz,
                "jnz": self.jnz,
                "ld": self.ld,
                "ldsp": self.ldsp,
                "st": self.st,
                "add": self.add,
                "sub": self.sub,
                "cmp": self.cmp,
                "inc": self.inc,
                "in": self.inn,
                "out": self.out,
                "ald": self.ald,
                "dec": self.dec,
                "jne": self.jne}
        self.save_program()

    def save_program(self):
        for row in self.program:
            if "opcode" in row and "arg" in row:
                self.datapath.memory[row["index"]] = {"opcode": row["opcode"], "arg": row["arg"], "term": row["term"], "direct": row["direct"]}
            elif "opcode" in row:
                self.datapath.memory[row["index"]] = {"opcode": row["opcode"], "term": row["term"]}
            else:
                self.datapath.memory[row["index"]] = {"arg" : row["arg"]}


    
    def decode_execute(self, instruction):
        logging.debug(self.datapath.__str__()+instruction["term"][2])

        if "arg" in instruction:
            self.datapath.dr = instruction["arg"]

            if instruction["direct"]:
                arg = self.datapath.dr
            else:
                arg = self.datapath.memory[self.datapath.dr]["arg"]

            self.commands[instruction["opcode"]](arg)

        else:
            self.commands[instruction["opcode"]]()
            

    
    def run(self):
        # Run the processor until halted
        self.running = True
        while self.running:
            instruction = self.datapath.memory[self.datapath.ar]

            self.decode_execute(instruction)
            self.datapath.ar = self.datapath.ip
            self.datapath.ip+=1
            if instruction is None:
                break  # End of program
    
    
    def hlt(self):
        self.running = False

    def neg(self):
        self.datapath.acc= - self.datapath.acc
        self.datapath.set_flags()

    def push(self):
        obj = self.datapath.acc
        self.datapath.memory[self.datapath.sp] = obj
        self.datapath.sp -=1

    def pop(self):
        self.datapath.acc = self.datapath.memory[self.datapath.sp]
        self.datapath.sp-=1
        self.datapath.set_flags()

    def jmp(self, arg):
        self.datapath.ip = self.datapath.dr
    
    def jz(self, arg):
        if self.datapath.Z == 1:
            self.datapath.ip = self.datapath.dr

    def jnz(self):
        if self.datapath.Z == 0:
            self.datapath.ip = self.datapath.dr
    
    def jne(self, arg):
        if self.datapath.N == 0:
            self.datapath.ip = self.datapath.dr
    
    def ld(self, arg):
        self.datapath.acc = arg
        self.datapath.set_flags()
        
    def ldsp(self):
        self.datapath.acc = self.datapath.sp
    
    def st(self, arg):
        self.datapath.memory[self.datapath.dr]["arg"] = self.datapath.acc

    def add(self, arg):
        self.datapath.acc += arg
        self.datapath.set_flags()
    
    def sub(self, arg):
        self.datapath.acc -= arg
        self.datapath.set_flags()


    def cmp(self, arg):
        self.datapath.acc -= arg
        self.datapath.set_flags()

    def inc(self, arg):
        self.datapath.memory[self.datapath.dr]["arg"] +=1

    def dec(self):
        self.datapath.acc-=1

    def inn(self):
        print("TODO")

    def out(self):
        print(self.datapath.acc)
    
    def ald(self):
        self.datapath.acc = self.datapath.memory[self.datapath.acc]["arg"]


