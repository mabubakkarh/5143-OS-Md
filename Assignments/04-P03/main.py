from modules.rand_inst_generator import *
from modules.pcb import *
from modules.dispatcher import *
import json
import time
from threading import Thread


class ReaderWriter:
    """
    """
    def __init__(self, writers):
        self.writers = writers
        #RandInstructions(privilegedRatio=0.3, sleepRatio=0.15, numProcesses=writers)        # Generate instructions
        self.load_instructions()
        self.start_dispatcher()

    def load_instructions(self):
        def extract_inst(inst_string):
            insts = inst_string.split(' ')
            if insts == ['']:
                return None
            output=[]
            if len(insts) == 3:
                if insts[0] == "READ":
                    op, block, memory, r1 = insts[0], insts[1][0], insts[1][1:], insts[2]
                elif insts[0] == "WRITE":
                    op, block, memory, r1 = insts[0], insts[1][0], insts[1][1:], insts[2]
                elif insts[0] == "LOAD":
                    op, block, memory, r1 = insts[0], insts[1], "", insts[2]
                else:
                    op, block, memory, r1 = insts[0], insts[1][0], insts[1][1:], insts[2]
                output=[op, block, memory, r1]     
            else:
                sleep, count= insts[0],  insts[1]
                output=[sleep, count]
            return output
            
        self.processes = list()
        for i in range(self.writers):
            obj = Pcb()
            self.processes.append(obj)

        for i in range(self.writers):
            inst_file_path = f"instructions/program_{i}.exe"
            file = open(inst_file_path, 'r')
            self.processes[i].open_files.append(inst_file_path)
            data = json.load(file)
            file.close()
            self.processes[i].open_files.remove(inst_file_path)

            self.processes[i].state = "ready"

            for instructions in data:
                for inst in instructions:
                    self.processes[i].instructions.append(extract_inst(inst))

    def start_dispatcher(self):
        self.dispatcher = Dispatcher()
        for process in self.processes:
            self.dispatcher.ready.append(process)

        threads = []
        t = Thread(target=self.dispatcher.print_progress_bar, args=())
        t.start()
        threads.append(t)


#                       ALL_THE_4_DISPATCHER_CALL
                   
        # self.dispatcher.schedule_with_priority() #Run1
        # self.dispatcher.schedule_without_priority() #Run2
        # change sleep
        # self.dispatcher.schedule_with_priority() #Run3
        self.dispatcher.schedule_without_priority() #Run4


        for t in threads:
            t.join()

obj = ReaderWriter(5)