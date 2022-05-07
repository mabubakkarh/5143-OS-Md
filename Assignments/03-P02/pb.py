from scheduler import Scheduler
from process import Process
# implementation of Priority-Based Scheduling
class PB(Scheduler):
    def __init__(self, process_input_list, cpu_count, priority_list):
        super().__init__(process_input_list, cpu_count)
        self.priority_list = priority_list

    def run(self):
        cur_time = 0
        finish_processes_count = 0
        at_idx = 0
        # sorted as priority
        sorted_processes = sorted(self.processes, key=lambda Process: Process.priority_list,reverse=True)

        while finish_processes_count < self.process_count:

            for process_idx in range(at_idx, self.process_count):
                process = sorted_processes[process_idx]
                if process.at == cur_time:
                    print("process arrived - cur_time:", cur_time, " p_id :", process.id)
                    self.ready_queue.append(process)
                elif process.at > cur_time:
                    at_idx = process_idx
                    break

            self.record_history(self.ready_queue[:], self.cpus, self.processes)

            for cpu in self.cpus:

                if cpu.is_finished():
                    print("process finished - cur_time:", cur_time, " p_id :", cpu.process.id)
                    cpu.process.calculate_finished_process(cur_time)
                    finish_processes_count += 1

                    cpu.set_idle()

                if cpu.is_idle():

                    if self.ready_queue:
                        cpu.set_process(self.ready_queue.pop(0))

            super().work()
            cur_time += 1

