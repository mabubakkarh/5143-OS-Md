import os
from turtle import clear

def printProgressBar (process_count, progress, status, total, wait_queue = [], priority_number = 0, length = 40, fill = '█', printEnd = "\r"):
    """
    Prints progress bar for 3 memory blocks, readers and writers
    """
    display = f"""
    \nProcess Status - \n"""
    for i in range(process_count):
        if total[i] == 0:
            filled_length = length
            percentage = 100
        else:
            filled_length = int(length * progress[i] // total[i])
            percentage = (progress[i]/total[i])*100
        bar = fill * filled_length + "-" * (length - filled_length)
        display += f"Process {i} | {bar} | Percentage : {percentage} | Status : {status[i]}\n"

    display += "Priority Wait Queue : "
    for item in wait_queue:
        display += str(item) + " "
    
    display += f"\nPriority Number : {priority_number}"
    
    os.system('clear')
    print(display, end=printEnd)
    if progress == total: 
        print()
