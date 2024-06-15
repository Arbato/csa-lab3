from datapath import DataPath
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
                "or": self.orr,
                "and": self.andd,
                "cmp": self.cmp,
                "inc": self.inc,
                "in": self.inn,
                "out": self.out,
                "ald": self.ald,
                "dec": self.dec}
        self.save_program()

    def save_program(self):
        for row in self.program:
            if "opcode" in row:
                self.datapath.memory[row["index"]] = {"opcode": row["opcode"], "arg": row["arg"], "term": row["term"], "direct": row["direct"]}
            else:
                self.datapath.memory[row["index"]] = {"arg" : row["arg"]}

        
        

    def fetch(self):

    
    def decode_execute(self, instruction):
        if instruction["direct"]:
            self.datapath.dr = 
       
    
    def run(self):
        # Run the processor until halted
        running = True
        while running:
            instruction = self.fetch()
            if instruction is None:
                break  # End of program
            running = self.decode_and_execute(instruction)
    
    
    def hlt(self):
        running = False

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

    def jmp(self):
        self.datapath.ip = self.datapath.dr
    
    def jz(self):
        if self.datapath.Z == 1:
            self.datapath.ip = self.datapath.dr

    def jnz(self):
        if self.datapath.Z == 0:
            self.datapath.ip = self.datapath.dr
    
    def ld(self):
        self.datapath.acc = self.datapath.memory[self.datapath.ar]
        self.datapath.set_flags()
        
    def ldsp(self):
        self.datapath.acc = self.datapath.sp
    
    def st(self):
        self.datapath.memory[self.datapath.ar] = self.datapath.acc

    def add(self):
        self.datapath.acc += self.datapath.dr
        self.datapath.set_flags()
    
    def sub(self):
        self.datapath.acc -= self.datapath.dr
        self.datapath.set_flags()

    def cmp(self):
        self.datapath.acc -= self.datapath.dr
        self.datapath.set_flags()

    def inc(self):
        self.datapath.acc+=1

    def dec(self):
        self.datapath.acc-=1

    def inn(self):
        print("TODO")

    def out(self):
        print("TODO")
    
    def ald(self):
        self.datapath.acc = self.datapath.memory[self.datapath.acc]


