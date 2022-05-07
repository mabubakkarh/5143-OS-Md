from typing import Counter


class Pcb:
    """
    Process control block
    """
    id_counter = 0
    def __init__(self):
        self.id = Pcb.id_counter 
        Pcb.id_counter += 1

        self.state = "new"      # new, ready, running, waiting, terminated
        self.priority = 1
        self.register_content = [int(), int()]
        self.pc = 0
        self.open_files = []
        self.address = [int(), int()]
        self.instructions = list()