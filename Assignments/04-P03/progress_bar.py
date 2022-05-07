import os

def printProgressBar (iteration, total, active_readers, active_writers, reader_count, writer_count, length = 70, fill = '█', printEnd = "\r"):
    """
    Prints progress bar for 3 memory blocks, readers and writers
    """
    filledLength1 = int(length * iteration[0] // total)
    filledLength2 = int(length * iteration[1] // total)
    filledLength3 = int(length * iteration[2] // total)
    bar1 = fill * filledLength1 + '-' * (length - filledLength1)
    bar2 = fill * filledLength2 + '-' * (length - filledLength2)
    bar3 = fill * filledLength3 + '-' * (length - filledLength3)
    
    os.system('clear')
    print(f"""
        Total Readers Active : {active_readers}
        Total Writers Active : {active_writers}
        Memory Block A |{bar1}| \n        Reader Count : {reader_count[0]} | Writer Count : {writer_count[0]}
        Memory Block B |{bar2}| \n        Reader Count : {reader_count[1]} | Writer Count : {writer_count[1]}
        Memory Block C |{bar3}| \n        Reader Count : {reader_count[2]} | Writer Count : {writer_count[2]}
    """, end= printEnd
    )

    if iteration == total: 
        print()