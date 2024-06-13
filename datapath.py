

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
