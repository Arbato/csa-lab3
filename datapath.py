

class DataPath:
    data_memory_size = None
    "Размер памяти данных."

    data_memory = None
    "Память данных. Инициализируется нулевыми значениями."

    data_address = None
    "Адрес в памяти данных. Инициализируется нулём."

    acc = None
    "Аккумулятор. Инициализируется нулём."

    input_buffer = None
    "Буфер входных данных. Инициализируется входными данными конструктора."

    output_buffer = None
    "Буфер выходных данных."
    def __init__(self, data_memory_size, input_buffer):
        assert data_memory_size > 0, "Data_memory size should be non-zero"
        self.data_memory_size = data_memory_size
        self.data_memory = [0] * data_memory_size
        self.data_address = 0
        self.acc = 0
        self.input_buffer = input_buffer
        self.output_buffer = []


class Datapath:
    def __init__(self, memory_size=256, register_count=4):
        # Initialize memory and registers
        self.memory = [0] * memory_size
        self.registers = [0] * register_count
        self.PC = 0  # Program counter
        
    def load_memory(self, index, value):
        # Load value into memory at specified index
        self.memory[index] = value
        
    def load_register(self, reg, value):
        # Load value into register at specified index
        self.registers[reg] = value
        
    def get_memory(self, index):
        # Retrieve value from memory at specified index
        return self.memory[index]
    
    def get_register(self, reg):
        # Retrieve value from register at specified index
        return self.registers[reg]
    
    def increment_pc(self):
        # Increment program counter
        self.PC += 1
    
    def set_pc(self, value):
        # Set program counter to a specific value
        self.PC = value
        
    def get_pc(self):
        # Get the current program counter value
        return self.PC