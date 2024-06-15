class DataPath:
    def __init__(self, memory_size=256):
        # Initialize memory and registers
        self.memory = [0] * memory_size
        self.acc = 0
        self.sp = memory_size
        self.dr = 0
        self.ar = 0
        self.ip = 0
        self.N = 0
        self.Z = 0

    def __str__(self):
        return (
            f"ACC: {self.acc:10} |" f"AR: {self.ar:5} |" f"IP: {self.ip:5} |" f"DR: {self.dr:10} |" f"SP: {self.sp:5} |")

    def load_instr_from_memory(self):
        # Load instruction from memory in adress register
        self.ar = self.ip
        self.ip+=1
        return self.memory[self.ar]
        
    def set_flags(self):
        if self.acc == 0:
            self.Z = 1
        else:
            self.Z = 0
        if self.acc < 0:
            self.N = 1
        else:
            self.N = 0
    def get_memory(self, index):
        # Retrieve value from memory at specified index
        return self.memory[index]
    
    def get_register(self, reg):
        # Retrieve value from register at specified index
        return self.registers[reg]
    

