from abc import ABCMeta, abstractmethod
from cpu import CPU


class Scheduler(metaclass=ABCMeta):
    # number of process count, process list , CPU list, Ready queue
    def __init__(self, process_input_list, cpu_count):
        self.process_count = len(process_input_list)
        self.processes = process_input_list
        self.cpu_count = cpu_count
        self.cpus = self.create_cpus()
        self.ready_queue = []
        self.history = []
    # saving history of a process
    def record_history(self, ready_queue, cpus, processes):
        record = []
        record.append(ready_queue)
        record.append([cpu.process for cpu in cpus])
        record.append(processes)
        self.history.append(record)
    # create new cpus
    def create_cpus(self):
        cpu_list = []
        for i in range(self.cpu_count):
            cpu_list.append(CPU(i + 1))
        return cpu_list
    # current working process
    def work(self):
        for cpu in self.cpus:
            if not cpu.is_idle():
                cpu.process.remain_bt -= 1
                cpu.work_time += 1

    # working cpu's count
    def get_cpu_keep_working_count(self, quantum=-1):
        cpu_work_continue_count = 0
        for cpu in self.cpus:
            if cpu.is_finished(quantum) or cpu.is_idle():
                cpu_work_continue_count += 1
        return cpu_work_continue_count - len(self.ready_queue)

    @abstractmethod
    def run(self):
        pass
