from csv import writer
from dis import Instruction
import sys
import random_instruction_generator
import json
import threading as thread
from threading import Thread
from contextlib import contextmanager
import time
from progress_bar import printProgressBar
from timeit import timeit
import logging
logging.basicConfig(filename="writer_logs.log", level=logging.INFO)

@contextmanager
def acquire_timeout(lock, timeout=1000):
    result = lock.acquire(timeout=timeout)
    yield result

global A, B, C      # Shared data
global rcA, rcB, rcC    # Reader Semaphores    
global wcA, wcB, wcC    # Writer semaphores
global inst_counter
global oper_counter
global active_reader_count
global active_writer_count
global total_writers

lockA = thread.Lock()   # Thread lock
lockB = thread.Lock()   # Thread lock
lockC = thread.Lock()   # Thread lock
master_lock = thread.Lock() # Thread lock

def extract_inst(inst_string):
    insts = inst_string.split('\n')
    if insts == ['']:
        return None
    
    if len(insts) == 3: # Reader
        mb1, mad1, r1 = insts[0].split(' ')[1][0], insts[0].split(' ')[1][1:], insts[0].split(' ')[2][1]  # First READ statement
        mb2, mad2, r2 = insts[1].split(' ')[1][0], insts[1].split(' ')[1][1:], insts[1].split(' ')[2][1]  # Second READ statement
        operation, r3, r4 = insts[2].split(' ')[0], insts[2].split(' ')[1][1], insts[2].split(' ')[2][1]  # Operation statement

    else:   # Writer
        mb1, mad1, r1 = insts[0].split(' ')[1][0], insts[0].split(' ')[1][1:], insts[0].split(' ')[2][1]  # First READ statement
        mb2, mad2, r2 = insts[1].split(' ')[1][0], insts[1].split(' ')[1][1:], insts[1].split(' ')[2][1]  # Second READ statement
        operation, r3, r4 = insts[2].split(' ')[0], insts[2].split(' ')[1][1], insts[2].split(' ')[2][1]  # Operation statement
        r5, mb3, mad3 = insts[3].split(' ')[1][1], insts[3].split(' ')[2][0], insts[3].split(' ')[2][1:]

    # print(r1, r2, mb1, mb2, mad1, mad2, operation)
    obj = random_instruction_generator.instruction(
        operation = operation,
        r1 = r1,
        r2 = r2,
        mb1 = mb1,
        mb2 = mb2,
        mad1 = mad1,
        mad2 = mad2
    )
    return obj

def perform_operation(operation_type, r1, r2):
    time.sleep(0.000000002)
    global oper_counter
    oper_counter += 1
    if operation_type == "ADD":
        return int(r1) + int(r2)
    if operation_type == 'SUB':
        return int(r1) - int(r2)
    if operation_type == 'MUL':
        return int(r1) * int(r2)
    if operation_type == 'DIV':
        if int(r2) == 0:
            return 0
        return int(r1) // int(r2)
    
def print_progress_bar():
    global A, B, C, rcA, rcB, rcC, inst_counter, active_reader_count, active_writer_count, total_writers
    while True:
        printProgressBar(
                iteration = [rcA, rcB, rcC],
                total = 6*total_writers,
                active_readers = active_reader_count,
                active_writers = active_writer_count,
                reader_count = [rcA, rcB, rcC],
                writer_count = [wcA, wcB, wcC]
            )
        time.sleep(0.3)
        if active_reader_count == 0 and active_writer_count == 0:
            time.sleep(0.1)
            if active_reader_count == 0 and active_writer_count == 0:
                return

def Reader(file_path):
    global A, B, C, rcA, rcB, rcC, inst_counter, active_reader_count, active_writer_count, total_writers
    logging.basicConfig(filename="writer_logs.log", level=logging.INFO)

    # Read instructions
    file = open(file_path, 'r')
    instructions = file.read()
    file.close()

    # Load instructions
    inst_strings = instructions.split("\n\n")
    inst_list = []
    for inst in inst_strings:
        inst_list.append(extract_inst(inst))

    # Execute instructions
    for inst in inst_list:
        f1, f2, f3 = 0, 0, 0    # Variable required flags
        if inst == None:    # NoneType instruction
            continue

        # ACQUIRE LOCKS
        if inst.mb1 == 'A' or inst.mb2 == 'A':
            if rcA == 0:
                with acquire_timeout(lockA) as acquired:
                    if not acquired:
                        print("Lock not acquired")
            
            f1 = 1  # Memory block A is being used in this instruction
            rcA += 1  # Reader count for block A 

        if inst.mb1 == 'B' or inst.mb2 == 'B':
            if rcB == 0:
                with acquire_timeout(lockB) as acquired:
                    if not acquired:
                        print("Lock not acquired")
            
            f2 = 1  # Memory block B is being used in this instruction
            rcB += 1    # Reader count for block B

        if inst.mb1 == 'C' or inst.mb2 == 'C':
            if rcC == 0:
                with acquire_timeout(lockC) as acquired:
                    if not acquired:
                        print("Lock not acquired")
            
            f3 = 1  # Memory block C is being used in this instruction
            rcC += 1    # Reader count for block C

        active_reader_count += 1

        # Critical Section Start
        if inst.mb1 == 'A':
            val1 = A[inst.mad1] 
        elif inst.mb1 == 'B':
            val1 = B[inst.mad1] 
        else:
            val1 = C[inst.mad1] 

        if inst.mb2 == 'A':
            val2 = A[inst.mad2]
        elif inst.mb2 == 'B':
            val2 = B[inst.mad2]
        else:
            val2 = C[inst.mad2]

        perform_operation(inst.operation, val1, val2)
        # Critical Section End

        inst_counter += 1

        # Releasing Locks
        if f1 == 1:
            rcA -= 1
            if rcA == 0:
                if lockA.locked():
                    lockA.release()
        if f2 == 1:
            rcB -= 1
            if rcB == 0:
                if lockB.locked():
                    lockB.release()
        if f3 == 1:
            rcC -= 1
            if rcC == 0:
                if lockC.locked():
                    lockC.release()

        active_reader_count -= 1

def Writer(file_path):
    global A, B, C, rcA, rcB, rcC, wcA, wcB, wcC, inst_counter, active_reader_count, active_writer_count, total_writers
    logging.basicConfig(filename="writer_logs.log", level=logging.INFO)

    # Read instructions
    file = open(file_path, 'r')
    instructions = file.read()
    file.close()

    # Load instructions
    inst_strings = instructions.split("\n\n")
    inst_list = []
    for inst in inst_strings:
        inst_list.append(extract_inst(inst))

    # Execute instructions
    for inst in inst_list:
        fw1, fw2, fw3 = 0, 0, 0 # Write lock flags
        if inst == None:    # Nonetype instruction
            continue

        # Acquire locks
        start = time.time()
        # WRITE LOCKS
        if inst.mb1 == 'A' or inst.mb2 == 'A':
            with acquire_timeout(lockA) as acquired:
                if not acquired:
                    print("Lock not acquired")
            
            fw1 = 1
            wcA += 1

        if inst.mb1 == 'B' or inst.mb2 == 'B':
            with acquire_timeout(lockB) as acquired:
                if not acquired:
                    print("Lock not acquired")
            
            fw2 = 1
            wcB += 1

        if inst.mb1 == 'C' or inst.mb2 == 'C':
            with acquire_timeout(lockC) as acquired:
                if not acquired:
                    print("Lock not acquired")

            fw3 = 1
            wcC += 1
        
        end = time.time()
        logging.info(f"Writer waited {end - start} seconds for acquiring lock, locked memory block {inst.mb2}")
        active_writer_count += 1

        printProgressBar(
            iteration = [rcA, rcB, rcC],
            total = 6*total_writers,
            active_readers = active_reader_count,
            active_writers = active_writer_count,
            reader_count = [rcA, rcB, rcC],
            writer_count = [wcA, wcB, wcC]
        )

        # Start Critical Section
        if inst.mb1 == 'A':
            val1 = A[inst.mad1] 
        elif inst.mb1 == 'A':
            val1 = B[inst.mad1]
        else:
            val1 = C[inst.mad1]

        if inst.mb2 == 'A':
            val2 = A[inst.mad2]
        elif inst.mb2 == 'B':
            val2 = B[inst.mad2]
        else:
            val2 = C[inst.mad2]

        result = perform_operation(inst.operation, val1, val2)

        if inst.mb1 == 'A':
            A[inst.mad1] = result
        if inst.mb1 == 'B':
            B[inst.mad1] = result
        if inst.mb1 == 'C':
            C[inst.mad1] = result
        # End Critical Section
        
        # Release Write locks
        inst_counter += 1
        if fw1 == 1:
            wcA -= 1
            if lockA.locked():
                lockA.release()
        if fw2 == 1:
            wcB -= 1
            if lockB.locked():
                lockB.release()
        if fw3 == 1:
            wcC -= 1
            if lockC.locked():
                lockC.release()

        active_writer_count -= 1

def full_block_reader(file_path):
    global A, B, C, rcA, rcB, rcC, inst_counter, active_reader_count, active_writer_count, total_writers

    # Read instructions
    file = open(file_path, 'r')
    instructions = file.read()
    file.close()

    # Load instructions
    inst_strings = instructions.split("\n\n")
    inst_list = []
    for inst in inst_strings:
        inst_list.append(extract_inst(inst))

    # Execute instructions
    for inst in inst_list:
        if inst == None:    # NoneType instruction
            continue

        # ACQUIRE LOCKS
        if active_reader_count == 0:
            with acquire_timeout(master_lock) as acquired:
                if not acquired:
                    print("Lock not acquired")
        
        rcA += 1
        rcB += 1
        rcC += 1
        active_reader_count += 1

        # Critical Section Start
        if inst.mb1 == 'A':
            val1 = A[inst.mad1] 
        elif inst.mb1 == 'B':
            val1 = B[inst.mad1] 
        else:
            val1 = C[inst.mad1] 

        if inst.mb2 == 'A':
            val2 = A[inst.mad2]
        elif inst.mb2 == 'B':
            val2 = B[inst.mad2]
        else:
            val2 = C[inst.mad2]

        perform_operation(inst.operation, val1, val2)
        # Critical Section End

        inst_counter += 1

        # Releasing Locks
        if active_reader_count == 1:
            if master_lock.locked():
                master_lock.release()

        rcA -= 1
        rcB -= 1
        rcC -= 1
        active_reader_count -= 1

def full_block_writer(file_path):
    global A, B, C, rcA, rcB, rcC, wcA, wcB, wcC, inst_counter, active_reader_count, active_writer_count, total_writers
    logging.basicConfig(filename="writer_logs.log", level=logging.INFO)

    # Read instructions
    file = open(file_path, 'r')
    instructions = file.read()
    file.close()

    # Load instructions
    inst_strings = instructions.split("\n\n")
    inst_list = []
    for inst in inst_strings:
        inst_list.append(extract_inst(inst))

    # Execute instructions
    for inst in inst_list:
        if inst == None:    # Nonetype instruction
            continue

        start = time.time()
        # Acquire locks
        with acquire_timeout(master_lock) as acquired:
            if not acquired:
                print("Lock not acquired")
        
        end = time.time()
        logging.info(f"Writer waited {end - start} seconds for acquiring lock, locked entire memory block")
        active_writer_count += 1

        printProgressBar(
            iteration = [rcA, rcB, rcC],
            total = 6*total_writers,
            active_readers = active_reader_count,
            active_writers = active_writer_count,
            reader_count = [rcA, rcB, rcC],
            writer_count = [wcA, wcB, wcC]
        )

        # Start Critical Section
        if inst.mb1 == 'A':
            val1 = A[inst.mad1] 
        elif inst.mb1 == 'A':
            val1 = B[inst.mad1]
        else:
            val1 = C[inst.mad1]

        if inst.mb2 == 'A':
            val2 = A[inst.mad2]
        elif inst.mb2 == 'B':
            val2 = B[inst.mad2]
        else:
            val2 = C[inst.mad2]

        result = perform_operation(inst.operation, val1, val2)

        if inst.mb1 == 'A':
            A[inst.mad1] = result
        if inst.mb1 == 'B':
            B[inst.mad1] = result
        if inst.mb1 == 'C':
            C[inst.mad1] = result
        # End Critical Section
        
        # Release locks
        inst_counter += 1
        if master_lock.locked():
            master_lock.release()

        active_writer_count -= 1


if __name__ == "__main__":
    # Loading critical section data
    logging.basicConfig(filename="writer_logs.log", level=logging.INFO)
    logging.info("\n\n PROGRAM EXECUTION START \n\n")
    file = open("memory.json")
    memory = json.load(file)
    file.close()

    total_writers = int(sys.argv[2])
    # total_writers = 5
    A, B, C = memory['A'], memory['B'], memory['C']
    rcA, rcB, rcC = 0, 0, 0
    wcA, wcB, wcC = 0, 0, 0
    inst_counter = 0
    oper_counter = 0
    active_reader_count = 0
    active_writer_count = 0
    
    print("Generating instruction files")

    random_instruction_generator.clear_instructions()
    random_instruction_generator.generate_n_instruction_files(no_of_writer_files=total_writers, no_of_reader_files=total_writers*5)

    printProgressBar(
        iteration=[0, 0, 0],
        total = 6*total_writers,
        active_readers = 0,
        active_writers = 0,
        reader_count = [0, 0, 0],
        writer_count = [0, 0, 0]
    )

    # Locking only the necessary memory block
    threads = []
    start_time = time.time()
    for i in range(total_writers):
        t = Thread(target=Writer, args=(f"instructions/inst_writer_{i}.txt",))
        t.start()
        threads.append(t)

    for i in range(total_writers*5):
        t = Thread(target=Reader, args=(f"instructions/inst_reader_{i}.txt",))
        t.start()
        threads.append(t)

    progress_bar_thread = Thread(target=print_progress_bar, args = ())
    progress_bar_thread.start()

    # Wait all threads to finish.
    for t in threads:
        t.join()

    progress_bar_thread.join()

    end_time = time.time()
    file = open('modified_memory.json', 'w')
    data = {
        "A": A,
        "B": B,
        "C": C
    }
    json.dump(data, file, indent=4)
    file.close()

    print("\n")
    print("Total instructions : ", inst_counter)
    print("Total operations : ", oper_counter)
    print("Total time taken by locking only specific memory block : ", end_time - start_time, " seconds")
    copy_ic, copy_oc, copy_tc = inst_counter, oper_counter, end_time - start_time


    time.sleep(6)
    logging.info("LOGS FOR LOCKING THE ENTIRE MEMORY BLOCK \n\n")


    # Locking the entire memory block
    rcA, rcB, rcC = 0, 0, 0
    wcA, wcB, wcC = 0, 0, 0
    inst_counter = 0
    oper_counter = 0
    active_reader_count = 0
    active_writer_count = 0


    threads = []
    start_time = time.time()
    for i in range(total_writers*5):
        t = Thread(target=full_block_reader, args=(f"instructions/inst_reader_{i}.txt", ))
        t.start()
        threads.append(t)

    for i in range(total_writers):
        t = Thread(target=full_block_writer, args=(f"instructions/inst_writer_{i}.txt", ))
        t.start()
        threads.append(t)

    progress_bar_thread = Thread(target=print_progress_bar, args = ())
    progress_bar_thread.start()

    # Wait all threads to finish.
    for t in threads:
        t.join()

    progress_bar_thread.join()

    end_time = time.time()
    file = open('modified_memory.json', 'w')
    data = {
        "A": A,
        "B": B,
        "C": C
    }
    json.dump(data, file, indent=4)
    file.close()

    logging.info("\n\n PROGRAM EXECUTION FINISHED \n\n")

    print("\n")
    print("LOCKING ENTIRE MEMORY BLOCK")
    print("Total instructions : ", inst_counter)
    print("Total operations : ", oper_counter)
    print("Total time taken : ", end_time - start_time, " seconds")

    print("\n")
    print("LOCKING REQUIRED MEMORY BLOCK")
    print("Total instructions : ", copy_ic)
    print("Total operations : ", copy_oc)
    print("Total time taken : ", copy_tc, " seconds")

    logging.info("No of writers : " + str(total_writers))
    logging.info("\n")
    logging.info("LOCKING ENTIRE MEMORY BLOCK")
    logging.info("Total instructions : " + str(inst_counter))
    logging.info("Total operations : " + str(oper_counter))
    logging.info("Total time taken : " + str(end_time - start_time) + " seconds")

    logging.info("\n")
    logging.info("LOCKING REQUIRED MEMORY BLOCK")
    logging.info("Total instructions : " + str(copy_ic))
    logging.info("Total operations : " + str(copy_oc))
    logging.info("Total time taken : " + str(copy_tc) + " seconds")

    
    

    