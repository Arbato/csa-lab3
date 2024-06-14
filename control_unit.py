



class ControlUnit:
    def __init__(self, datapath, program):
        self.datapath = datapath
        self.program = program
    
    def fetch(self):
        # Fetch the instruction at the current PC
        pc = self.datapath.get_pc()
        if pc < len(self.program):
            return self.program[pc]
        return None
    
    def decode_and_execute(self, instruction):
        # Decode the instruction and execute it
        if 'opcode' in instruction:
            opcode = instruction['opcode']
            arg = instruction.get('arg', None)
            
            if opcode == 'jmp':
                # Jump to the specified address
                self.datapath.set_pc(arg)
            elif opcode == 'ld':
                # Load value into register
                if instruction['direct']:
                    value = arg
                else:
                    value = self.datapath.get_memory(arg)
                self.datapath.load_register(instruction['term'][0], value)
                self.datapath.increment_pc()
            elif opcode == 'add':
                # Add value to register
                if instruction['direct']:
                    value = arg
                else:
                    value = self.datapath.get_memory(arg)
                reg = instruction['term'][0]
                self.datapath.load_register(reg, self.datapath.get_register(reg) + value)
                self.datapath.increment_pc()
            elif opcode == 'st':
                # Store value from register to memory
                reg = instruction['term'][0]
                self.datapath.load_memory(arg, self.datapath.get_register(reg))
                self.datapath.increment_pc()
            elif opcode == 'hlt':
                # Halt the processor
                print("Halting execution.")
                return False  # Stop execution
        else:
            # No operation instruction (possibly just data)
            self.datapath.increment_pc()
        
        return True  # Continue execution
    
    def run(self):
        # Run the processor until halted
        running = True
        while running:
            instruction = self.fetch()
            if instruction is None:
                break  # End of program
            running = self.decode_and_execute(instruction)
