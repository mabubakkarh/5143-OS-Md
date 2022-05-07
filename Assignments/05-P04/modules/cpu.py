from wsgiref.simple_server import software_version
from rich import print
from modules.register import *
from modules.alu import *
from modules.lock import Lock
import json
import time
from datetime import datetime

with open("memory.json") as file:
    shared_data = json.load(file)

class Cpu:
    def __init__(self, register_count):
        self.pc = 0
        self.registers = [Register()]*(register_count+1)
        self.alu = Alu(self.registers)
        self.priority_registers = [Register()]*(register_count+1)
        self.priority_number = 0
        self.software_lock = ""

    def execute_instruction_with_priority(self, instruction, time_quanta, pid, process_count):
        if self.software_lock == "":
            self.software_lock = [Lock()]*process_count

        if len(instruction) ==2:    #SLEEP
            if float(instruction[1]) > 5:
                instruction[1] = float(instruction[1])/10

            if float(instruction[1]) < time_quanta:
                time.sleep(float(instruction[1]))
                return [True, Lock.waitQ, self.priority_number]
            else:
                time.sleep(time_quanta)
                instruction[1] = float(instruction[1]) - time_quanta
            if instruction[1] <= 0:
                return [True, Lock.waitQ, self.priority_number]
            return [False, Lock.waitQ, self.priority_number]

        if instruction[0]=='READ':
            mb = instruction[1]
            mad = instruction[2]
            reg = int(instruction[3][1])
            self.registers[reg].write(shared_data[mb][mad])

        elif instruction[0]=='WRITE':
            mb = instruction[3][0]
            mad = instruction[3][1:]
            reg = int(instruction[2])
            shared_data[mb][mad] = self.registers[reg].read()

        elif instruction[0] == "LOAD":
            reg = int(instruction[3][1]) - 2
            val = int(instruction[1])

            if reg == 2:
                if self.priority_number == val:
                    self.software_lock[pid].acquire()
                    self.priority_number += 1
                    self.priority_registers[reg].write(val)
                    self.software_lock[pid].release()
                    return [True, Lock.waitQ, self.priority_number]
                else:
                    self.software_lock[pid].wait()
                    return [False, Lock.waitQ, self.priority_number]
        else:
            self.alu.exec(instruction[0])  # ALU instruction

        return [True, Lock.waitQ, self.priority_number]

    def execute_instruction_without_priority(self, instruction, time_quanta):
        if len(instruction) ==2:    #SLEEP
            if float(instruction[1]) > 5:
                instruction[1] = float(instruction[1])/10

            if float(instruction[1]) < time_quanta:
                time.sleep(float(instruction[1]))
                return True
            else:
                time.sleep(time_quanta)
                instruction[1] = float(instruction[1]) - time_quanta
            if instruction[1] <= 0:
                return True
            return False

        if instruction[0]=='READ':
            mb = instruction[1]
            mad = instruction[2]
            reg = int(instruction[3][1])
            self.registers[reg].write(shared_data[mb][mad])

        elif instruction[0]=='WRITE':
            mb = instruction[3][0]
            mad = instruction[3][1:]
            reg = int(instruction[2])
            shared_data[mb][mad] = self.registers[reg].read()

        elif instruction[0] == "LOAD":
            reg = int(instruction[3][1]) - 2
            val = int(instruction[1])
            self.priority_registers[reg].write(val)

        else:
            self.alu.exec(instruction[0])  # ALU instruction

        return True

    def save_results(self):
        cou = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        with open(f"memory_modified_{cou}.json", 'w') as file:
            json.dump(shared_data, file, indent=4)