from random import shuffle, randint
import os

class instruction:
    def __init__(self, operation, r1, r2, mb1, mb2, mad1, mad2):
        self.operation = operation
        self.r1, self.r2 = r1, r2
        self.mb1, self.mb2 = mb1, mb2
        self.mad1, self.mad2 = mad1, mad2

    def get_inst_string(self, reader_flag=1):
        """
        @param reader_flag: 1 = reader, 0 = writer
        """
        inst = ""
        inst += f"READ {self.mb1}{self.mad1} {self.r1}\n"
        inst += f"READ {self.mb2}{self.mad2} {self.r2}\n"
        inst += f"{self.operation} {self.r1} {self.r2}\n"
        if reader_flag == 0:
            inst += f"WRITE {self.r1} {self.mb1}{self.mad1}\n"
        return inst


def generate_instruction():
    operations = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memory_blocks = ["A", "B", "C"]
    memory_address = [x for x in range(100, 255, 5)]

    shuffle(operations)
    shuffle(registers)
    shuffle(memory_blocks)
    shuffle(memory_address)

    obj = instruction(
        operation = operations[0],
        r1 = registers[0],
        r2 = registers[1],
        mb1 = memory_blocks[0],
        mb2 = memory_blocks[1],
        mad1 = memory_address[0],
        mad2 = memory_address[1]
    )

    return obj

def generate_n_instructions(no_of_instructions, file_path, reader_flag = 1):
    file = open(file_path, 'w')
    for _ in range(no_of_instructions):
        inst = generate_instruction()
        file.write(inst.get_inst_string(reader_flag=reader_flag))
        file.write("\n")

def generate_n_instruction_files(no_of_writer_files, no_of_reader_files):
    for i in range(no_of_writer_files):
        file_name = f"instructions/inst_writer_{i}.txt"
        no_of_instructions = randint(100, 500)
        generate_n_instructions(
            no_of_instructions = no_of_instructions,
            file_path = file_name,
            reader_flag=0
        )
    
    for i in range(no_of_reader_files):
        file_name = f"instructions/inst_reader_{i}.txt"
        no_of_instructions = randint(100, 500)
        generate_n_instructions(
            no_of_instructions = no_of_instructions,
            file_path = file_name,
            reader_flag=1
        )

def clear_instructions():
    dir = 'instructions/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))