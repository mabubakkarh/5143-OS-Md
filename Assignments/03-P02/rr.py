from scheduler import Scheduler

# implementation of Round-Robin

class RR(Scheduler):
    def __init__(self, process_input_list, cpu_count, quantum):
        super().__init__(process_input_list, cpu_count)
        self.quantum = quantum

    def run(self):
        cur_time = 0
        finish_processes_count = 0
        at_idx = 0
        sorted_processes = sorted(self.processes, key=lambda x: x.at)

        while finish_processes_count < self.process_count:

            for process_idx in range(at_idx, self.process_count):
                process = sorted_processes[process_idx]
                if process.at == cur_time:
                    print("processe arrived - cur_time:", cur_time, " p_id :", process.id)
                    self.ready_queue.append(process)
                elif process.at > cur_time:
                    at_idx = process_idx
                    break


            self.record_history(self.ready_queue[:], self.cpus, self.processes)

            cpu_keep_working_count = self.get_cpu_keep_working_count(self.quantum)

            for cpu in self.cpus:

                if cpu.is_finished(self.quantum):

                    if cpu.process.remain_bt > 0:

                        if cpu_keep_working_count > 0:
                            cpu_keep_working_count -= 1
                            cpu.work_time = 0
                            continue
                        self.ready_queue.append(cpu.process)
                        print("processe arrived again - cur_time:", cur_time, " p_id :", cpu.process.id)
                    else:

                        print("processe finished - cur_time:", cur_time, " p_id :", cpu.process.id)
                        cpu.process.calculate_finished_process(cur_time)
                        finish_processes_count += 1

                    cpu.set_idle()


                if cpu.is_idle():

                    if self.ready_queue:
                        cpu.set_process(self.ready_queue.pop(0))


            cur_time += 1
            super().work()
