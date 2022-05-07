from modules.cpu import Cpu
import time
from modules.progress_bar import *

class Dispatcher:
    def __init__(self):
        self.cpu = Cpu(2)
        self.time_quanta = 0.1 # in s

        self.ready = []
        self.running = []
        self.terminated = []
        self.waitQ = []
        self.priority_number = 0

    def print_progress_bar(self):
        while True:
            process_count = len(self.ready) + len(self.running) + len(self.terminated)
            progress = [0]*process_count
            status = [""]*process_count
            total = [0]*process_count
            for p in self.ready:
                status[p.id] = p.state
                progress[p.id] = p.pc
                total[p.id] = len(p.instructions)
            for p in self.running:
                status[p.id] = p.state
                progress[p.id] = p.pc
                total[p.id] = len(p.instructions)
            for p in self.terminated:
                status[p.id] = p.state
                progress[p.id] = p.pc
                total[p.id] = len(p.instructions)

            printProgressBar(
                process_count= process_count,
                progress= progress,
                status = status,
                total= total,
                wait_queue= self.waitQ,
                priority_number=self.priority_number
            )
        
            time.sleep(0.0005)
            if len(self.terminated) == process_count:
                time.sleep(0.01)
                if len(self.terminated) == process_count:
                    return

    def switch(self):
        if self.running != []:
            self.running[0].state = "ready"
            self.ready.append(self.running.pop())

        if self.ready != []:
            self.running.append(self.ready.pop(0))
            self.running[0].state = "running"
        else:
            print("All processes completed")
            self.cpu.save_results()
            return 1
        return 0

    def end_process(self, process):
        process.state = "terminated"
        self.terminated.append(process)
        self.running.pop(0)
        return self.switch()

    def schedule_without_priority(self):
        self.switch()
        while True:
            start = float(time.time())
            rprocess = self.running[0]
            total_instructions = len(rprocess.instructions)
    
            while (float(time.time()) - start) < self.time_quanta:
                if self.cpu.execute_instruction_without_priority(rprocess.instructions[rprocess.pc], self.time_quanta):
                    rprocess.pc += 1
                if rprocess.pc == total_instructions:
                    if self.end_process(rprocess):
                        return
                break
            self.switch()

    def schedule_with_priority(self):
        self.switch()
        process_count = len(self.ready) + len(self.running) + len(self.terminated)
        while True:
            start = time.time()
            rprocess = self.running[0]
            total_instructions = len(rprocess.instructions)

            while time.time() - start < 0.01:
                if rprocess.pc < len(rprocess.instructions):
                    flag, self.waitQ, self.priority_number = self.cpu.execute_instruction_with_priority(
                        rprocess.instructions[rprocess.pc], self.time_quanta, rprocess.id, process_count)
                    if flag:
                        rprocess.pc +=1
                if rprocess.pc == total_instructions:
                    flag = self.end_process(rprocess)
                    if flag == 1:
                        return
                    break
                        
            self.switch()
            

